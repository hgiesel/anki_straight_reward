declare DIR="$(cd "$(dirname "$0")/.." && pwd -P)"
mkdir -p "$DIR/build"

if [[ "$1" =~ ^-?a$ ]]; then
  # for uploading to AnkiWeb
  declare addon_id='957961234'
else
  # for installing myself
  declare addon_id='straight_reward'
fi

cd "$DIR/dist"

zip -r "$DIR/build/$addon_id.ankiaddon" *
