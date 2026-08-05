using System.Reflection;
using System.Text;
using Hydra;
using Newtonsoft.Json;

// Dumps every DLCS.HydraModel resource type's property flags as markdown, for
// cross-checking the docs' | domain | range | readonly | writeonly | tables
// (hygiene sprint ruling XC-09). Usage:
//   dotnet run [-p:ProtagonistSrc=<path-to-protagonist/src/protagonist>] -- "<context note>" > out.md
// The optional first argument is printed into the header (e.g. the git SHA the
// dump was generated against).

var asm = typeof(DLCS.HydraModel.Customer).Assembly;
var contextNote = args.Length > 0 ? args[0] : "(no context note supplied)";

var sb = new StringBuilder();
sb.AppendLine("# DLCS.HydraModel property flags");
sb.AppendLine();
sb.AppendLine($"> GENERATED FILE — do not edit by hand; re-run `tools/hydra-model-dump` instead.");
sb.AppendLine($"> Source: {asm.GetName().Name}. Context: {contextNote}");
sb.AppendLine(">");
sb.AppendLine("> Per XC-09: docs tables and these attributes must agree. A mismatch is a card-level");
sb.AppendLine("> decision (either side may hold the intended contract), not a silent fix.");

var resourceTypes = asm.GetTypes()
    .Where(t => t is { IsClass: true, IsPublic: true } && !t.IsSubclassOf(typeof(global::Hydra.Model.Class)))
    .OrderBy(t => t.Name);

foreach (var type in resourceTypes)
{
    var rows = type.GetProperties(BindingFlags.Public | BindingFlags.Instance | BindingFlags.DeclaredOnly)
        .Select(p => new
        {
            Property = p,
            Json = p.GetCustomAttribute<JsonPropertyAttribute>(),
            Supported = p.GetCustomAttribute<SupportedPropertyAttribute>()
        })
        .Where(x => x.Json?.PropertyName != null && x.Supported != null)
        .OrderBy(x => x.Json!.Order)
        .ToList();

    if (rows.Count == 0)
    {
        continue;
    }

    sb.AppendLine();
    sb.AppendLine($"## {type.Name}");
    sb.AppendLine();
    sb.AppendLine("| property | kind | range | readonly | writeonly |");
    sb.AppendLine("|:---|:---|:---|:---|:---|");
    foreach (var row in rows)
    {
        var kind = row.Supported is HydraLinkAttribute ? "link" : "field";
        var range = (row.Supported!.Range ?? "")
            .Replace("http://www.w3.org/2001/XMLSchema#", "xsd:")
            .Replace("http://www.w3.org/ns/hydra/core#", "hydra:");
        sb.AppendLine(
            $"| {row.Json!.PropertyName} | {kind} | {range} | {row.Supported.ReadOnly} | {row.Supported.WriteOnly} |");
    }
}

Console.Write(sb.ToString());
