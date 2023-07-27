import os

# Iterate on all analysis:
for analysis in Model.Analyses:
    savePath = analysis.AnalysisSettings.SolverFilesDirectory

    res_names = []
    collected_data = {}

    # Iterate on all the result objects:
    for sol in analysis.Solution.Children:
        try:
            sol_data = sol.PlotData
        except Exception:
            ExtAPI.Log.WriteMessage("Could not get data for {}".format(sol.Name))
            continue

        unit = sol_data["Values"].Unit
        sol_name = "{} [{}]".format(sol.Name, unit)
        res_names.append(sol_name)

        for body, node, value in zip(
            sol_data["Body"], sol_data["Node"], sol_data["Values"]
        ):
            collected_data.setdefault(body, {})
            collected_data[body].setdefault(node, {})

            collected_data[body][node][sol_name] = value

    # Export the data to csv
    csv_path = os.path.join(savePath, analysis.Name + ".csv")

    with open(csv_path, "w") as f:
        f.write("{};{};{}\n".format("Body", "Node", ";".join(res_names)))

        for body, nodes in collected_data.items():
            for node, solutions in nodes.items():
                results = [str(solutions.get(res, "n/a")) for res in res_names]
                f.write("{};{};{}\n".format(body, node, ";".join(results)))
