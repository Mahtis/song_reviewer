#!/bin/bash

echo "I FEEL SO ALIVE"
docker run -ti --rm -v `pwd`:/essentia mtgupf/essentia essentia_streaming_extractor_music $1 $2
echo "I am done"
