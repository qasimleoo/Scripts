declare -A paths_and_days=(
  ["/opt/tomcat/conf/crawlerfiles/czds/gtld/full"]=6
  ["/opt/tomcat/conf/crawlerfiles/czds/gtld/update"]=6
)

delete_old_items() {
  local path="$1"
  local days="$2"
  local cutoff_date=$(date -d "$days days ago" +%Y-%m-%d)  # Calculate cutoff date

  cd "$path" || { echo "Error: Cannot cd to $path"; return 1; }

  local items=(*)
  local has_only_folders=true

  for item in "${items[@]}"; do
    if [[ ! -d "$item" ]]; then
      has_only_folders=false
      break
    fi
  done

  if $has_only_folders; then
    for folder in */; do
      folder=${folder%/}  # Remove trailing slash
      folder_date=""

      if [[ $folder =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
        folder_date="$folder"
      else
        if [[ $folder =~ ([0-9]{4}-[0-9]{2}-[0-9]{2}) ]]; then
          folder_date="${BASH_REMATCH[1]}"
        else
          echo "Skipping folder without a valid date: $folder"
          continue
        fi
      fi

      if [[ "$folder_date" < "$cutoff_date" ]]; then
        sudo rm -r "$folder"
        echo "Deleted folder: $folder"
      fi
    done
  else
    for item in *; do
      item_date=""

      if [[ $item =~ ([0-9]{4}-[0-9]{2}-[0-9]{2}) ]]; then
        item_date="${BASH_REMATCH[1]}"
      else
        echo "Skipping item without a valid date: $item"
        continue
      fi

      if [[ "$item_date" < "$cutoff_date" ]]; then
        sudo rm -r "$item"
        echo "Deleted item: $item"
      fi
    done
  fi
}

for path in "${!paths_and_days[@]}"; do
  delete_old_items "$path" "${paths_and_days[$path]}"