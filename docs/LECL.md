Runnable Interface:


LangChain Expression Language
    LangChain Expression language is a declarative approach to create new Runnables.
    Runnables created using LECL is called a chain.
    chain is a Runnable implementing Runnable interface.

Benefits of LECL
    Optimized Parrallel execution : langChain's Batch execution reduce the latency as processing can be done in 
    parallel instead of sequentially

    Guaranteed Async Support : Chains can be run asynchronously in the server environment

    Simplify Streaming

If you have a simple chain (e.g., prompt + llm + parser, simple retrieval set up etc.), LCEL is a reasonable fit, if you're taking advantage of the LCEL benefits.

Composition Primitives:
    LECL chains are built by using existing Runnable interfaces.
    The Composition primitives are RunnableSequence and RunnableParallel

Runnable Sequence :
    Allows you to chain multiple Runnables Sequentially
    Output of one of the Runnable acting as an input for the next

        from langchain_core.runnables import RunnableSequence
        chain = RunnableSequence([runnable1, runnable2])

        final_output = chain.invoke(some_input)

RunnableParallel
    RunnableParallel is a composition primitive that allows you to run multiple runnables concurrently, with the same input provided to each.

How "yield" works in Python:
    create a generator functions
    step 1 : execute the function till you reach a yield statement
    step 2 : pause the execution of the function by saving its state
    step 3 : return the value to the caller
    step 4 : if caller invokes another time, resume the execution of the function and do step 1

Its more efficient than copying elements to the list

Common LECLs
