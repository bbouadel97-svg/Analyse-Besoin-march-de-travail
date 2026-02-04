**Quick Context**
- **Repo type:**: .NET multi-project console apps (TargetFramework: net10.0).
- **Layout:**: root project `Newapp.csproj` plus a `myproj26/` folder containing `App2/`, `App3/`, and `NewClass/` projects.

**Build & Run (most useful commands)**
- **Build solution:**: `dotnet build` from the repo root (or run against a specific project folder).
- **Run a project:**: `dotnet run --project myproj26/App2/App2.csproj` (or point to other `*.csproj`).
- **Open in IDE:**: open the root in Visual Studio / VS Code and use the normal launch tasks; solution file present as `GlobalSolution.slnx`.

**Where to look first**
- **Entry points:**: `Program.cs` files at the repo root and under `myproj26/App2/` and `myproj26/App3/` (simple console apps). See [Program.cs](Program.cs) and [myproj26/App2/Program.cs](myproj26/App2/Program.cs).
- **Project files:**: `Newapp.csproj`, `myproj26/App2/App2.csproj`, `myproj26/App3/App3.csproj`, and `myproj26/NewClass/newclass.csproj` define targets and framework (net10.0).
- **README:**: high-level notes live in [myproj26/README.md](myproj26/README.md).

**Project-specific patterns & conventions**
- **Target framework:**: projects use `net10.0` and enable `ImplicitUsings` and `Nullable` — prefer nullable-aware code and rely on implicit global usings where present.
- **Minimal console apps:**: `Program.cs` files are minimal single-file consoles (use of top-level statements). When adding features, follow the same minimal-program style.
- **Multiple small projects:**: treat each folder under `myproj26/` as an independent runnable project; changes should be localized unless intentionally cross-project.

**Integration points & notable quirks**
- **Solution file:**: `GlobalSolution.slnx` exists but may not be required for `dotnet` commands; you can build projects directly.
- **Potential csproj issue:**: `myproj26/App2/App2.csproj` contains an extra stray character in the `<PropertyGroup>` (syntax hint). CI/builders will surface this — validate `dotnet build` if edits are made.
- **No external packages observed:**: projects have no obvious `PackageReference` entries; check `*.csproj` if you add dependencies.

**How to change code safely**
- **Avoid editing `bin/` or `obj/`:** those are generated.
- **Keep changes small & local:** modify the `myproj26/<Project>/` project when adding features to that app.
- **Build frequently:** run `dotnet build` after edits; run the specific project with `dotnet run --project <path>`.

**Examples (copyable)**
- Build root: `dotnet build`.
- Build specific project: `dotnet build myproj26/App2/App2.csproj`.
- Run specific project: `dotnet run --project myproj26/App3/App3.csproj`.

**When in doubt**
- Look at the project's `Program.cs` and its `.csproj` to understand intent and enabled features.
- If builds fail, run `dotnet build -v:n` to get more diagnostics.

If any areas are unclear or you'd like this file to include contributing rules, commit conventions, or CI instructions, tell me which section to expand.
