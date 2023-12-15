#!/usr/bin/env bash

# Get the date, first 4 chars of branch name and short commit hash
date=$(date -u +"%Y%m%d")
branch=${1:-$(git rev-parse --abbrev-ref HEAD | cut -c1-4)}
commit=${2:-$(git rev-parse --short HEAD)}

# Function to transform characters to ZMK key behaviours
transform_char() {
    local char=$1
    if [[ $char =~ [A-Za-z] ]]; then
        echo "<&kp ${char^^}>, "
    elif [[ $char =~ [0-9] ]]; then
        echo "<&kp N${char}>, "
    elif [ "$char" = "." ]; then
        echo "<&kp DOT>, "
    fi
}

# Iterate over the date and format characters
formatted_date=""
for ((i = 0; i < ${#date}; i++)); do
    formatted_date+=$(transform_char "${date:$i:1}")
done

# Insert separator between date and branch
formatted_date+="<&kp MINUS>, "

# Iterate over the branch and format characters
formatted_branch=""
for ((i = 0; i < ${#branch}; i++)); do
    formatted_branch+=$(transform_char "${branch:$i:1}")
done

# Insert separator between branch and commit hash
formatted_branch+="<&kp MINUS>, "

# Iterate over the commit hash and format characters
formatted_commit=""
for ((i = 0; i < ${#commit}; i++)); do
    formatted_commit+=$(transform_char "${commit:$i:1}")
done

# Combine the formatted string, add trailing carriage return
formatted_result="$formatted_date$formatted_branch$formatted_commit"
formatted_result+="<&kp RET>"

echo $formatted_result
# Create new macro to define version, overwrite previous one

echo '#define VERSION_MACRO' > "config/version.dtsi"
echo 'macro_ver: macro_ver {' >> "config/version.dtsi"
echo 'compatible = "zmk,behavior-macro";' >> "config/version.dtsi"
echo 'label = "macro_ver";' >> "config/version.dtsi"
echo '#binding-cells = <0>;' >> "config/version.dtsi"
echo "bindings = $formatted_result;" >> "config/version.dtsi"
echo '};' >> "config/version.dtsi"
