#!/usr/bin/env bash
LineId=0

while IFS= read -r line || [[ -n "$line" ]]; do #Checking if all the lines are in correct format
    if [[ ! "$line" =~ ^\[([^\]]+)\]\ \[([^\]]+)\]\ (.*) ]]; then
        echo "Line format invalid"
        exit 1
    fi
done < $1
echo "LineId,Time,Level,Content,EventId,EventTemplate" > $2

while IFS= read -r line || [[ -n "$line" ]]; do #parsing the file based on the regex and content
    if [[ "$line" =~ ^\[([^\]]+)\]\ \[([^\]]+)\]\ (.*) ]]; then
        Time="${BASH_REMATCH[1]}"
        Level="${BASH_REMATCH[2]}"
        Content="${BASH_REMATCH[3]}"
        ((LineId++))
    fi

    if [[ "$Content" =~ jk2_init\(\)\ Found\ child\ .*\ in\ scoreboard\ slot\ .* ]];then
        EventId="E1"
        EventTemplate="jk2_init() Found child <*> in scoreboard slot <*>"
    elif [[ "$Content" =~ workerEnv\.init\(\)\ ok\ .* ]];then        
        EventId="E2"
        EventTemplate="workerEnv.init() ok <*>"-
    elif [[ "$Content" =~ mod_jk\ child\ workerEnv\ in\ error\ state\ .* ]];then
        EventId="E3"
        EventTemplate="mod_jk child workerEnv in error state <*>"
    elif [[ "$Content" =~ \[client\ .*\]\ Directory\ index\ forbidden\ by\ rule:\ .* ]];then
        EventId="E4"
        EventTemplate="[client <*>] Directory index forbidden by rule: <*>"
    elif [[ "$Content" =~ jk2_init\(\)\ Can\'t\ find\ child\ .*\ in\ scoreboard ]];then
        EventId="E5"
        EventTemplate="jk2_init() Can't find child <*> in scoreboard"
    elif [[ "$Content" =~ mod_jk\ child\ init\ .*\ .* ]];then
        EventId="E6"
        EventTemplate="mod_jk child init <*> <*>"
    else
        continue
    fi

    CleanContent=$(echo "$Content" | tr -d '\n' | tr -d '\r' | tr -s ' ' )
    echo "$LineId,$Time,$Level,$CleanContent,$EventId,$EventTemplate" >> $2
done < $1