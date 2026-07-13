def execute_plan(plan):

    results = []

    for step in plan:

        print(f"[PLAN] {step}")

        results.append(
            f"Completed: {step}"
        )

    return "\n".join(results)
