# Itération 5 - Gestion des clés à l'échelle d'un parc

## Objectif

Passer d'une machine isolée à une organisation capable de gérer les clés et les
moyens de récupération pendant tout leur cycle de vie.

## Feuille de l'itération

- formaliser génération, stockage, sauvegarde, récupération, rotation,
  révocation et destruction ;
- répartir les responsabilités et les moyens de secours ;
- mettre en œuvre systemd-cryptenroll/TPM2 ou Clevis/Tang ;
- comparer cette approche avec les services de gestion de clés cloud.

## Livrable attendu

Une architecture de gestion des clés d'un parc, avec choix techniques,
responsabilités, procédure de récupération et limites identifiées.

- [Concevoir une gestion des clés adaptée à un parc de machines](concevoir-gestion-cles-parc.md)
- [Option 1 - systemd-cryptenroll et TPM2](option-systemd-cryptenroll-tpm2.md)
- [Option 2 - Clevis et Tang](option-clevis-tang.md)
- [Termes à retenir](../../pense-bete/glossaire/securite-donnees/it-5.md)
