declare DIR="$(cd "$(dirname "$0")/.." && pwd -P)"

rm -rf "$DIR/dist/*"

# for filename in "$DIR/designer/"*'.ui'; do
#   pyuic5 "$filename" > "$DIR/gui/forms/$(basename ${filename%.*})_ui.py"
# done

cp -rf "$DIR/__init__.py" \
  "$DIR/manifest.json" \
  "$DIR/src" \
  "$DIR/user_files" \
  "$DIR/dist"

yarn --cwd "$DIR/web" build

echo 'Was successfully compiled!'
