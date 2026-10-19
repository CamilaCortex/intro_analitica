# Cómo usar esta plantilla

```bash
cp -r 09-Proyecto-Final/plantilla_repo ../proyecto-<equipo>
cd ../proyecto-<equipo>
mv gitignore.txt .gitignore
rm LEEME_PLANTILLA.md
uv init --python 3.14 --no-readme --name proyecto-<equipo>
uv add pandas numpy matplotlib seaborn scikit-learn jupyter ipykernel joblib fastapi "uvicorn[standard]" httpx
uv add --dev pytest ruff
git init && git add . && git commit -m "feat: estructura inicial desde la plantilla"
```

> El `.gitignore` se llama `gitignore.txt` dentro de la plantilla para que no afecte al repositorio del curso.
