DROP TABLE IF EXISTS EMPLOYEE_ID;

CREATE TABLE EMPLOYEE_ID
(
    EMP_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY
);

DROP TABLE IF EXISTS EMPLOYEE;

CREATE TABLE EMPLOYEE(
    EMP_ID VARCHAR(7) NOT NULL PRIMARY KEY DEFAULT '0',
    EMP_NAME VARCHAR(30) NOT NULL,
    EMP_BOD DATE NOT NULL,
    EMP_ADDRESS VARCHAR(30) NOT NULL,
    EMP_PHONE VARCHAR(13) NOT NULL
);

DELIMITER $$

CREATE TRIGGER EMPLOYEE_ID_TRIG
BEFORE INSERT ON EMPLOYEE
FOR EACH ROW
    BEGIN
        INSERT INTO EMPLOYEE_ID VALUES(DEFAULT);
        SET NEW.EMP_ID = CONCAT('u', LPAD(LAST_INSERT_ID(), 6, '0'));
    END $$
    DELIMITER ;

INSERT INTO EMPLOYEE VALUES 
(DEFAULT, 'FELIX', '2001-01-12', 'Malang', '087892314322'), 
(DEFAULT, 'FEBRIAN', '2001-02-02', 'Malang', '087832321231');