#Integration tests
Integration tests for this library.


Uses [raspi/docker-powerdns-travis-ci-rest-test](https://github.com/raspi/docker-powerdns-travis-ci-rest-test) docker image.

Pull from Docker hub:

    docker pull raspi/docker-powerdns-travis-ci-rest-test
    
Run on machine:
    
    docker run -p 8081:8081 raspi/docker-powerdns-travis-ci-rest-test

Then run:
  
    python3 -m unittest discover -v tests_integration