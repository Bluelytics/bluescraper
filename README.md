# bluescraper

```
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 151654911502.dkr.ecr.us-west-2.amazonaws.com
docker build -t bluelytics_scraper .
docker tag bluelytics_scraper:latest 151654911502.dkr.ecr.us-west-2.amazonaws.com/bluelytics_scraper:latest
docker push 151654911502.dkr.ecr.us-west-2.amazonaws.com/bluelytics_scraper:latest
```