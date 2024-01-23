CREATE DATABASE MasterMinds;

USE MasterMinds;

CREATE TABLE PlayerData(
	name TEXT,
	gameID int AUTO_INCREMENT,
	moves TEXT,
	attempts int,
	gameComplete boolean,
	PRIMARY KEY (gameID)
);



INSERT INTO PlayerData (name, moves, attempts, gameComplete) VALUES ('Alice', 'red,blue,green,orange', '1', 1);
INSERT INTO PlayerData (name, moves, attempts, gameComplete) VALUES ('Bob', 'purple,magenta,orange,blue;red,green,white,magenta;blue,green,orange,red', '3', 1);
INSERT INTO PlayerData (name, moves, attempts, gameComplete) VALUES ('Charlie', 'white,orange,red,magenta;green,blue,white,orange;red,magenta,blue,green', '3', 1);
INSERT INTO PlayerData (name, moves, attempts, gameComplete) VALUES ('David', 'green,blue,orange,magenta;purple,white,red,blue;orange,magenta,red,white;white,orange,red,magenta;green,blue,white,orange', '5', 0);
INSERT INTO PlayerData (name, moves, attempts, gameComplete) VALUES ('Emma', 'magenta,white,green,red;blue,orange,purple,magenta', '2', 1);
INSERT INTO PlayerData (name, moves, attempts, gameComplete) VALUES ('Frank', 'blue,green,white,magenta;orange,red,blue,green;white,magenta,orange,red;green,red,orange,purple;white,orange,red,magenta;green,blue,white,orange;red,magenta,blue,green', '7', 0);
INSERT INTO PlayerData (name, moves, attempts, gameComplete) VALUES ('Grace', 'orange,red,purple,blue;green,magenta,white,orange;purple,blue,green,magenta', '3', 1);
INSERT INTO PlayerData (name, moves, attempts, gameComplete) VALUES ('Hannah', 'red,white,orange,blue;green,magenta,purple,red;orange,blue,green,magenta;blue,orange,purple,magenta', '4', 1);
INSERT INTO PlayerData (name, moves, attempts, gameComplete) VALUES ('Ian', 'purple,blue,magenta,orange', '1', 0);
INSERT INTO PlayerData (name, moves, attempts, gameComplete) VALUES ('Jessica', 'green,orange,red,magenta;blue,white,purple,green', '2', 0);
INSERT INTO PlayerData (name, moves, attempts, gameComplete) VALUES ('Kevin', 'white,purple,magenta,orange;blue,green,red,purple;magenta,orange,blue,green;blue,green,white,magenta;orange,red,blue,green;white,magenta,orange,red', '6', 1);
INSERT INTO PlayerData (name, moves, attempts, gameComplete) VALUES ('Lily', 'orange,magenta,red,blue;green,white,orange,magenta;red,blue,green,white', '3', 0);
INSERT INTO PlayerData (name, moves, attempts, gameComplete) VALUES ('Mike', 'red,blue,green,orange;purple,magenta,white,red;green,orange,purple,magenta;red,white,orange,blue;green,magenta,purple,red;orange,blue,green,magenta', '6', 1);
INSERT INTO PlayerData (name, moves, attempts, gameComplete) VALUES ('Natalie', 'blue,green,white,magenta;orange,red,blue,green;white,magenta,orange,red', '3', 0);
INSERT INTO PlayerData (name, moves, attempts, gameComplete) VALUES ('Olivia', 'green,orange,purple,blue;red,white,magenta,green;purple,blue,red,white', '3', 0);
INSERT INTO PlayerData (name, moves, attempts, gameComplete) VALUES ('Peter', 'orange,red,magenta,blue;green,purple,white,orange;magenta,blue,green,purple;green,red,blue,orange', '4', 1);
INSERT INTO PlayerData (name, moves, attempts, gameComplete) VALUES ('Quinn', 'red,magenta,blue,green', '1', 1);
INSERT INTO PlayerData (name, moves, attempts, gameComplete) VALUES ('Rachel', 'magenta,blue,green,orange;red,white,purple,magenta', '2', 1);
INSERT INTO PlayerData (name, moves, attempts, gameComplete) VALUES ('Simon', 'blue,green,orange,magenta;white,red,blue,green;orange,magenta,white,red;red,white,purple,magenta;green,orange,red,white', '5', 0);
INSERT INTO PlayerData (name, moves, attempts, gameComplete) VALUES ('John', 'blue,red,black,orange;yellow,blue,green,pink', '2', 0);



CREATE USER 'webapp'@'%' IDENTIFIED BY 'masterminds1';

GRANT ALL ON MasterMinds.* TO 'webapp'@'%';

