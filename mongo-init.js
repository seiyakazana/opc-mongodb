db = db.getSiblingDB('mydb');

db.createUser({
  user: 'db_admin',
  pwd: 'db_admin_pwd',
  roles: [
    { role: 'dbOwner', db: 'mydb' }
  ]
});

db.createUser({
  user: 'app_user',
  pwd: 'app_user_pwd',
  roles: [
    { role: 'readWrite', db: 'mydb' }
  ]
});