import beaker
import pyteal as pt
from pyteal import *

app = beaker.Application("guessing_word")


class GuessState:
    hidden_word = beaker.GlobalStateValue(
        stack_type=pt.TealType.bytes, default=pt.Bytes("")
    )
    word = beaker.LocalStateValue(
        stack_type=pt.TealType.bytes, default=pt.Bytes("No word")
    )
    player_one = beaker.GlobalStateValue(
        stack_type=pt.TealType.bytes,
        descr=" Account of the first player-word setter",
        default=pt.Bytes("No player one"),
    )
    player_two = beaker.GlobalStateValue(
        stack_type=pt.TealType.bytes,
        descr="Account of the second player-word guesser",
        default=pt.Bytes("No player two"),
    )
    wager = beaker.GlobalStateValue(
        stack_type=pt.TealType.uint64,
        descr="Betting amount",
        default=pt.Int(0),
    )
    cntr = beaker.GlobalStateValue(
        stack_type=pt.TealType.uint64,
        descr="Counter of tries",
        default=pt.Int(0),
    )
    print = beaker.GlobalStateValue(stack_type=pt.TealType.bytes, default=pt.Bytes(""))


app = beaker.Application("guessing_word", state=GuessState)


@app.create(bare=True)
def create() -> pt.Expr:
    return app.initialize_global_state()


@app.opt_in(bare=True)
def opt_in() -> pt.Expr:
    return pt.Seq(
        pt.If(app.state.player_one.get() == pt.Bytes("No player one"))
        .Then(app.state.player_one.set(pt.Txn.sender()))
        .ElseIf(app.state.player_two.get() == pt.Bytes("No player two"))
        .Then(app.state.player_two.set(pt.Txn.sender()))
        .Else(pt.Reject()),
        app.initialize_local_state(addr=pt.Txn.sender()),
    )


@app.external
def play(
    word: pt.abi.String, payment: pt.abi.PaymentTransaction, *, output: pt.abi.String
) -> pt.Expr:
    pom = pt.abi.String()
    pt.Assert(payment.get().receiver() == pt.Global.current_application_address())

    return pt.Seq(
        pt.If(app.state.player_one.get() == Txn.sender())
        .Then(
            pt.Seq(
                app.state.hidden_word.set(word.get()),
                app.state.print.set(
                    pt.Bytes("You have successfully setted the word for guessing!")
                ),
                pom.set(app.state.print.get()),
                output.set(pom),
            )
        )
        .Else(
            pt.Seq(
                app.state.word.set(word.get()),
                app.state.print.set(pt.Bytes("Check the result of guessing.")),
                pom.set(app.state.print.get()),
                output.set(pom),
            )
        ),
        app.state.wager.set(payment.get().amount()),
    )


@app.external
def game_result(opponent: pt.abi.Account, *, output: pt.abi.String) -> pt.Expr:
    return pt.Seq(
        pt.If(
            pt.And(
                (app.state.player_two.get() == Txn.sender()),
                app.state.cntr.get() < pt.Int(3),
                app.state.word.get() != app.state.hidden_word.get(),
            )
        )
        .Then(
            output.set("Bad guess. Try again."),
            app.state.cntr.set(app.state.cntr.get() + pt.Int(1)),
        )
        .ElseIf(
            pt.And(
                (app.state.player_two.get() == Txn.sender()),
                app.state.cntr.get() < pt.Int(3),
                app.state.word.get() == app.state.hidden_word.get(),
            )
        )
        .Then(
            output.set("Congratulations! Money is transfered to your account!"),
            app.state.hidden_word.set(app.state.hidden_word.default),
            pay(pt.Int(0), app.state.wager.get()),
        )
        .ElseIf(
            pt.And(
                (app.state.player_one.get() == Txn.sender()),
                (app.state.hidden_word.get() == app.state.hidden_word.default),
            )
        )
        .Then(
            output.set("You lost."),
            pay(pt.Int(1), app.state.wager.get()),
        )
        .ElseIf(
            pt.And(
                (app.state.player_one.get() == Txn.sender()),
                app.state.cntr.get() >= pt.Int(3),
            )
        )
        .Then(
            output.set("Congratulations! Money is transfered to your account!"),
            pay(pt.Int(0), app.state.wager.get()),
        )
        .ElseIf(
            pt.And(
                (app.state.player_two.get() == Txn.sender()),
                app.state.cntr.get() >= pt.Int(3),
                app.state.word.get() != app.state.hidden_word.get(),
            )
        )
        .Then(
            output.set("You don't have any tries left. You lost! :("),
            pay(pt.Int(1), app.state.wager.get()),
        )
    )


@pt.Subroutine(pt.TealType.none)
def pay(acc_index: pt.Expr, amount: pt.Expr) -> pt.Expr:
    return pt.InnerTxnBuilder.Execute(
        {
            pt.TxnField.type_enum: pt.TxnType.Payment,
            pt.TxnField.fee: pt.Int(1000),
            pt.TxnField.amount: amount,
            pt.TxnField.receiver: pt.Txn.accounts[acc_index],
        }
    )


@app.external
def sum_of_fees(*, output: pt.abi.Uint64) -> pt.Expr:
    totalFees = ScratchVar(TealType.uint64)
    i = ScratchVar(TealType.uint64)
    return Seq(
        i.store(Int(0)),
        totalFees.store(Int(0)),
        While(i.load() < Global.group_size()).Do(
            totalFees.store(totalFees.load() + Gtxn[i.load()].fee()),
            i.store(i.load() + Int(1)),
        ),
        output.set(totalFees.load()),
    )


@app.external
def word_length(*, output: pt.abi.Tuple2[pt.abi.String, pt.abi.Uint64]) -> pt.Expr:
    counter = pt.abi.Uint64()
    word = pt.abi.String()
    return pt.Seq(
        counter.set(Len(app.state.hidden_word.get())),
        word.set(Bytes("Number of letters:")),
        output.set(word, counter),
    )
