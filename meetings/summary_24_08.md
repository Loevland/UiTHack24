# Oppsummering Møte 24.08

## Tema
Avstemning om følgende temaer, satser på å ha bestemt tema innen 3. September
- Cyberpunk
- Cartoon
- Game of Thrones
- Lord of The Rings
- Post-apocalyptic/Space/Aliens

## Repo
- Alle skal ha tilgang til GitHub repoet
- Vi prøver å bruke toolet [ctfcli](https://github.com/CTFd/ctfcli) for å pushe oppgaver inn i CTFd (for å slippe å gjøre det manuelt). Alle oppgaver må dermed ha en `challenge.yml` hver hvor oppgavetekst, poeng, opplastede file, challenge author (hvis ønskelig), osv. er spesifisert. Eksempel-template for `challenge.yml` ligger i `/` på repoet under navnet `challenge-example.yml` (ikke alle feltene trenger å være fylt inn, det er spesifisert hvilke felter som er required).

## Infrastruktur
- CTFd som platform (samme som i tidsligere år)
- Isolerte containere per lag
    - Status: Jobbes med å prøve å sette opp en slik løsning
    - Kjører på samme måte som i fjor hvis det skulle vise seg at vi ikke får satt opp i tide
- Kunne vært en fordel å hatt en mailserver til registrering/glemt passord, men er ikke noe som prioriteres for øyeblikket
    - Alternativt kreve discord-login. Denne muligheten undersøkes, men har ikke sett noe offisielt repo som støtter dette

## Hints
- Forslag om å gå vekk i fra hints som koster poeng, siden man bare kan lage en ny bruker for å kjøpe hints for å slippe å tape poeng på "hovedbrukeren". Spillerne slipper også å risikere å miste poeng ved å kjøpe et hint som ikke hjelper de (enten at de ikke er kommet til det steget, eller kommet lengre)
    - Alternativ løsning; Bruke et ticket-system på Discord til å gi hints på oppgaver under X antall poeng. Spillerne oppgir i ticketen hvor langt de er kommet, og hva de har prøvd, så kan vi gi små hints for å vise en retning å gå i
    - Pros:
        - Spillerne kan få mer nyttige hints, og risikerer ikke å stå bom fast på de oppgavene under X poeng (som nok blir de enklere/lav middels oppgavene)
        - Slipper en haug med DMs, og har alt på ett sted

    - Cons:
        - Må følge med på discord ticket-kanalen (dette har vi vel forsåvidt allerede brukt å gjøre tidligere)

## Discord Bot
- Discord bot er satt om slik at spillerne kan lage tickets hvis de f.eks ikke får til å kjøre en oppgave, noe er galt, eller andre ting (evt. hints også om vi går for den løsningen)

- Med Admin-rollen skal alle ha tilgang til tickets-kanalene
    - *support*: Spillerne reagerer på meldingen til boten for å opprette en ticket, en thread lages da for spilleren hvor vi admins kan joine
    - *tickets*: Alle aktive tickets i form av threads
    - *tickets-archive*: Arkiv av lukkede tickets. Her kan man se på tidligere tickets som har blitt svart på
- Alle Admin burde ha tilgang til Dashboardet til boten gjennom linken i botens profil. Her kan vi konfigurere boten

## Noob challs
- Prøver å gå over til Docker-containere istedet for å ha alle inne på ssh
    - Da slipper vi å risikere at noe er satt opp feil slik at spillerne får annen tilgang på TD-serveren enn ønsket
- Formatet på noob-challengene blir fortsatt helt lik som tidligere, bare med netcat tilkobling istedet for ssh tilkobling