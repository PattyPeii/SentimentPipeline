# SentimentPipeline

This repo is merely a decoration for our project in order to make it more interesting and to properly utilize rabbitmq.

## To deploy ml sevice

Note: This service is not unlimit, we have only 500 requests per month.

```
docker build -t cooknet/sentiment-consumer .
docker run -d --network="host" --name workspace_consumer cooknet/sentiment-consumer
```

Please make sure that docker host is pointing to rabbitmq host

## Example procedure

- comment(POST)
- publisher(nodejs) push message to queue 
- consumer(python) recieve message and do sentiment analysis 
- consumer save result to mongodb

### Example POST

recipe_id should be passed as a req.params.recipe_id

```
{
    "feedback_id": "10",
    "user_id": "2",
    "comment": "This formula is working so well, easy and delicious."
}
```

### Example result

```
{
    "_id":{"$oid":"6355506aea726aea1dea47f9"},
    "feedback_id":"3","user_id":"3",
    "recipe_id":"1",
    "comment":"This formula is working so well, easy and delicious.",
    "sentiment":"positive"
}
```
