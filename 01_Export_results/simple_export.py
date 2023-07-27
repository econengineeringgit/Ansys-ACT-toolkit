import os

# Iterate on all analysis:
for analysis in Model.Analyses:
    savePath = analysis.AnalysisSettings.SolverFilesDirectory

    # Iterate on all the result objects:
    for sol in analysis.Solution.Children:
        exportPath = os.path.join(savePath, sol.Name + ".txt")

        # Export data if possible (Not possible for example for "Solution Information")
        try:
            sol.ExportToTextFile(exportPath)
        except Exception:
            ExtAPI.Log.WriteMessage("Could not export data for {}".format(sol.Name))
