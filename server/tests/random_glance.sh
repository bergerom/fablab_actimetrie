#!/usr/bin/env bash
# Simule une personne (= un arduino) qui regarde d'autres personnes alternativement
# Utilisation ./random glance nb_personnes id_personne

if [ "$1" == "" ] || [ "$2" == "" ]; then
	echo "Utilisation : ./random_glance.sh [Nombre de participants] [Id de la personne]"
	exit 1
fi

# On prend l'adresse spécifiée dans la ligne de commande en priorité
if [ "$3" == "" ]; then
	url="http://localhost:3000/event"
else
	url="$3"
fi

nb_persons="$1"
my_id="$2"
for i in {1..15}
do
    looking_at=$(( (RANDOM % ($nb_persons)) + 1))
    if [ "$looking_at" -ne "$my_id" ]; then
        curl --data "ownId=""$my_id""&otherId=""$looking_at" "$url"
	echo ''
    fi
    sleep $(( (RANDOM % 2) + 1 ))
done;
