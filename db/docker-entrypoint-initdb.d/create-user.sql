create user 'api'@'%' identified by "yagg27";
grant all privileges on deployments.* to 'api'@'%';
grant all privileges on deployments_tests.* to 'api'@'%';
