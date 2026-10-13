from pathlib import Path
import re
p = Path("index.html")
if not p.exists():
    raise SystemExit("Place ce fichier dans le dossier contenant index.html.")
s = p.read_text(encoding="utf-8")
original = s

s = s.replace(
    "ChronoMap V15.5.5 — Géolocalisation",
    "ChronoMap V15.6.3 — Cartes historiques"
)

# Supprime les emprises urbaines synthétiques qui créent les gros aplats artificiels.
start = s.find("  // Reconstruction progressive du tissu urbain :")
end = s.find("  const buildRanges={", start)
if start != -1 and end != -1:
    s = s[:start] + (
        "  // Emprises urbaines synthétiques retirées : elles créaient des aplats artificiels.\\n"
        "  const footprintPhases=[];\\n\\n"
    ) + s[end:]

# Retire les grands disques circulaires correspondant aux points historiques.
s = s.replace(
    "      historicalVectorLayer.addLayer(L.circleMarker(f.coords,{pane:'historicalPane',radius:8+7*t,stroke:false,fillColor:'#9a663d',fillOpacity:.72,interactive:false}));\n      return;",
    "      // Les points historiques restent dans la fiche chronologique, sans cercle sur la carte.\n      return;"
)

# Retire le voile beige qui recouvrait toute la carte.
s = s.replace(
    "  const eraWash=L.rectangle(bounds,{pane:'historicalPane',stroke:false,fillColor:'#efe5cc',fillOpacity:.30*(1-presentProgress),interactive:false});\n"
    "  historicalVectorLayer.addLayer(eraWash);",
    "  // Aucun voile artificiel n'est ajouté au-dessus du fond cartographique."
)

s = s.replace(
    "const visibleFeatures=allFeatures.concat(footprintPhases);",
    "const visibleFeatures=allFeatures;"
)

if s == original:
    raise SystemExit("Aucune modification appliquée : les blocs attendus n'ont pas été trouvés. Fichier inchangé.")

# Sauvegarde l'original avant remplacement.
backup = Path("index.html.backup")
if not backup.exists():
    backup.write_text(original, encoding="utf-8")
p.write_text(s, encoding="utf-8")
print("OK — index.html corrigé. Sauvegarde : index.html.backup")
