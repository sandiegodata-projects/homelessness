#!/usr/bin/env bash

PROFILE=$1
BUCKET=ds.civicknowledge.org
ROOT_URL=http://$BUCKET
BASE_S3=s3://$BUCKET


IMAGES_PREFIX=downtownsandiego.org/homeless-count
BASE_IMAGES=$BASE_S3/$IMAGES_PREFIX


# Update images
aws s3 ls $BASE_IMAGES --recursive | awk -v ROOT_URL=$ROOT_URL '{print ROOT_URL"/"$4}' | grep '.png' > urls.txt
aws --profile $PROFILE s3 cp urls.txt $BASE_IMAGES/urls.txt
aws --profile $PROFILE s3api put-object-acl --bucket $BUCKET --key $IMAGES_PREFIX/urls.txt --acl public-read


# Update counts
ANNO_PREFIX=downtownsandiego.org/complete_annotations/count
BASE_ANNO=$BASE_S3/$ANNO_PREFIX

aws s3 ls $BASE_ANNO --recursive | awk -v ROOT_URL=$ROOT_URL '{print ROOT_URL"/"$4}' | grep '.json' > urls.txt
aws --profile $PROFILE s3 cp urls.txt $BASE_ANNO/urls.txt
aws --profile $PROFILE s3api put-object-acl --bucket $BUCKET --key $ANNO_PREFIX/urls.txt --acl public-read

# Update gcp
ANNO_PREFIX=downtownsandiego.org/complete_annotations/gcp
BASE_ANNO=$BASE_S3/$ANNO_PREFIX

# Update counts
aws s3 ls $BASE_ANNO --recursive | awk -v ROOT_URL=$ROOT_URL '{print ROOT_URL"/"$4}' | grep '.json' > urls.txt
aws --profile $PROFILE s3 cp urls.txt $BASE_ANNO/urls.txt
aws --profile $PROFILE s3api put-object-acl --bucket $BUCKET --key $ANNO_PREFIX/urls.txt --acl public-read

