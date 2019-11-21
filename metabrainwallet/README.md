# Brainwallet

## Google Translate API Key

ID: brainwallet-1573921011875
Service account, starting-account-43t7oxohtak0

## Setup

https://cloud.google.com/translate/docs/basic/setup-basic

. .env

```bash
curl -s -X POST -H "Content-Type: application/json" \
    -H "Authorization: Bearer "$(gcloud auth application-default print-access-token) \
    --data "{
  'q': 'The Great Pyramid of Giza (also known as the Pyramid of Khufu or the
        Pyramid of Cheops) is the oldest and largest of the three pyramids in
        the Giza pyramid complex.',
  'source': 'en',
  'target': 'es',
  'format': 'text'
}" "https://translation.googleapis.com/language/translate/v2"
```

key is in lastpass note on brainwallet
conda create -n brainwallet python=3.7 python
conda activate brainwallet

