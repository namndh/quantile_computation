## Techcombank Interview Coding Test

### Problem definition:
- In my opinion, the requirement of the test is to create an application with two APIs that:
    - Add or update a pool of values 
    - Compute the quantile value of a pool with known p-th percentile
### Installation:
- Requirement: `docker`, `docker-compose`
- To build a new container: `docker-compose build`
- To up the container: `docker-compose up`
### Solution
- The algorithm I used in this project:
    - Let `n` be the length of the `sorted_pool` and `0 < p <= 100` be the desired percentile.
    - If `n = 1` return the unique array element (regardless of the value of `p`); otherwise
    - Compute the estimated percentile position in the array `pos = (p * (n + 1) / 100)` and the difference, `d` between `pos` and `floor(pos)`.
    - If `pos < 1` return the smallest element in the array.
    - Else if `pos >= n` return the largest element in the array.
    - Else let `lower = sorted_pool[floor(pos)-1]` and let `upper = sorted_pool[floor(pos)]` (in Python, array start with 0). Return `lower + d * (upper - lower)`
- APIs:
    - `http://127.0.0.1:5000/pool` - it takes a json form that contains id of the pool and its value as input, it is used to update value of a pool or insert a new pool. A pool is defined as a dictionary with key is its id and value is list of its samples  
    - `http://127.0.0.1:5000/quantile` - it takes a json form that contains id of the pool and the p-th percentile as input, it is used to compute p-th percentile value of a pool
- You can use: `Postman`, `curl` or the add-on `Swagger` in the url: `http://127.0.0.1:5000` to test the API    
### Contributing
Pull request are welcome. Please open any issues to help me improve the project
### Reference
- [Apache Commons Math API docs](https://commons.apache.org/proper/commons-math/javadocs/api-3.5/org/apache/commons/math3/stat/descriptive/rank/Percentile.html)
- [Quantile: Definition and How to Find Them in Easy Steps](https://www.statisticshowto.com/quantile-definition-find-easy-steps/)

    

