## Techcombank Interview Coding Test

### Problem definition:
- In my opinion, the requirement of the test is to compute the quantile value of a list of number with known p-th percentile
- To solve the problem, I provide an API `quantile` which takes the input - a json form of the list named `pool` and the p-th percentile named `percentile`
- The algorithm I used in this project is:
    - Let `n` be the length of the `sorted_pool` and `0 < p <= 100` be the desired percentile.
    - If `n = 1` return the unique array element (regardless of the value of `p`); otherwise
    - Compute the estimated percentile position in the array (with Python, array starts with 0) `pos = (p * (n + 1) / 100) - 1` and the difference, `d` between `pos` and `floor(pos)`.
    - If `pos < 1` return the smallest element in the array.
    - Else if `pos >= n` return the largest element in the array.
    - Else let `lower = sorted_pool[floor(pos)]` and let `upper = sorted_pool[floor(pos) + 1]`. Return `lower + d * (upper - lower)`
### Installation:
- Requirement: `docker`, `docker-compose`
- To build a new container: `docker-compose build`
- To up the container: `docker-compose up`
### Usage
- Main API which uses to compute quantile value:
    - `http://0.0.0.0:5000/quantile`
- You can use: `Postman`, `curl` or the add-on Swagger in the url: `http://0.0.0.0:5000` to test the API    
### Contributing
Pull request are welcome. Please open any issues to help me improve the project
### Reference
- [Apache Commons Math API docs](https://commons.apache.org/proper/commons-math/javadocs/api-3.5/org/apache/commons/math3/stat/descriptive/rank/Percentile.html)
- [Quantile: Definition and How to Find Them in Easy Steps](https://www.statisticshowto.com/quantile-definition-find-easy-steps/)

    

