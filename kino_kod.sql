drop table Filmy cascade;
drop table Seanse cascade;
drop table Pracownicy cascade;
drop table Rezerwacje cascade;
drop table Ocz_rezerwacje cascade;
drop table Sale cascade;
CREATE TABLE Filmy (
    tytul varchar(40) primary key,
    czas_wyswietlania integer not null,
    opis varchar(1000) ,
    rok_produkcji integer not null check (rok_produkcji >= 1888 and rok_produkcji < 2023)
);
CREATE TABLE Pracownicy(
    id_pracownika char(6) primary key,
    haslo varchar(30) not null,
    imie varchar(30) not null,
    nazwisko varchar(30) not null
    
);
CREATE TABLE Sale (
    numer_sali smallint primary key,
    liczba_miejsc integer
);
CREATE TABLE Seanse (
    id_seansu  Serial primary key,
    godzina_rozpoczecia timestamp,
    sea_film varchar(40) references Filmy (tytul),
    sea_sala smallint references Sale(numer_sali)
);

CREATE TABLE Ocz_rezerwacje (
    id_ocz_rezerwacji SERIAL primary key,
    zajmowane_miejsca integer not null,
    rez_seans integer references Seanse(id_seansu)

);
CREATE TABLE Rezerwacje (
    id_rezerwacji integer not null,
    zajmowane_miejsca integer not null,
    rez_seans integer references Seanse(id_seansu)

);

CREATE OR REPLACE FUNCTION rezerwuj (ile_miejsc integer, id_seansu integer)
RETURNS integer AS $$
	INSERT INTO Rezerwacje(zajmowane_miejsca, rez_seans)
	values (ile_miejsc, id_seansu) RETURNING id_rezerwacji;
$$ LANGUAGE 'sql';

CREATE OR REPLACE FUNCTION add_seans (tytul varchar(40),czas timestamp,nr_sali smallint)
RETURNS integer AS $$
	INSERT INTO Seanse(godzina_rozpoczecia, sea_film, sea_sala)
	values (czas,tytul,nr_sali) RETURNING id_seansu;
$$ LANGUAGE 'sql';

CREATE OR REPLACE FUNCTION sprawdz_miejsca (seans_var integer)
RETURNS bigint AS $$
	select (liczba_miejsc - SUM(zajmowane_miejsca)) AS result from 
    (select id_rezerwacji,zajmowane_miejsca,numer_sali,liczba_miejsc,id_seansu 
    from rezerwacje left join (select sale.numer_sali,sale.liczba_miejsc,seanse.id_seansu
    from sale right join seanse on numer_sali=sea_sala) as foo on rez_seans=id_seansu where id_seansu=seans_var)
    as foo1 group by liczba_miejsc;
$$ LANGUAGE 'sql';

CREATE OR REPLACE FUNCTION sprawdz_ocz_miejsca (seans_var integer)
RETURNS bigint AS $$
	select (liczba_miejsc - SUM(zajmowane_miejsca)) AS result from 
    (select id_ocz_rezerwacji,zajmowane_miejsca,numer_sali,liczba_miejsc,id_seansu 
    from ocz_rezerwacje left join (select sale.numer_sali,sale.liczba_miejsc,seanse.id_seansu
    from sale right join seanse on numer_sali=sea_sala) as foo on rez_seans=id_seansu where id_seansu=seans_var)
    as foo1 group by liczba_miejsc;
$$ LANGUAGE 'sql';



CREATE OR REPLACE FUNCTION sprawdz_rezerwowane_miejsca (seans_var integer)
RETURNS bigint AS $$
	select (sprawdz_miejsca(seans_var) - SUM(zajmowane_miejsca)) AS result from 
    (select id_ocz_rezerwacji,zajmowane_miejsca,numer_sali,liczba_miejsc,id_seansu 
    from ocz_rezerwacje left join (select sale.numer_sali,sale.liczba_miejsc,seanse.id_seansu
    from sale right join seanse on numer_sali=sea_sala) as foo on rez_seans=id_seansu where id_seansu=seans_var)
    as foo1 group by liczba_miejsc;
$$ LANGUAGE 'sql';



insert into Filmy values ('Terminator','128','Arnold jest robotem i kogos tam chroni','1996');
insert into Filmy values ('Terminator 2','129','Arnold jest robotem i kogos tam bije','1997');
insert into Filmy values ('Terminator 3','130','Arnold jest robotem i ktos go bije','2001');
insert into Filmy values ('Fast and furious','140','Sa autka i sa szybkie','2002');
insert into Filmy values ('Fast and furious: Tokyo drift', '137','Sa autka w Japonii i tez sa szybkie','2003');
insert into Filmy values ('Fast and furious 3','111','Autka w Ameryce i Vin Diesel z rodzina','2010');

insert into Sale values ('1','57');
insert into Sale values ('2','63');
insert into Sale values ('3','54');
insert into Sale values ('4','56');
insert into Sale values ('5','25');

insert into Pracownicy values ('000000','haslo','Michal','Karcz');
insert into Pracownicy values ('000001','haslo','Jakub','Stankiewicz');
insert into Pracownicy values ('000002','haslo','Magdalena','Kowalska');


insert into Seanse (godzina_rozpoczecia, sea_film, sea_sala) values ('2023-01-19 18:00:00','Terminator','1');
insert into Seanse(godzina_rozpoczecia, sea_film, sea_sala) values ('2023-01-19 17:30:00','Terminator 2','2');
insert into Seanse(godzina_rozpoczecia, sea_film, sea_sala) values ('2023-01-19 19:00:00','Terminator 3','3');
insert into Seanse(godzina_rozpoczecia, sea_film, sea_sala) values ('2023-01-19 18:00:00','Fast and furious','4');
insert into Seanse(godzina_rozpoczecia, sea_film, sea_sala) values ('2023-01-20 20:00:00','Terminator','2');
insert into Seanse(godzina_rozpoczecia, sea_film, sea_sala) values ('2023-01-19 19:00:00','Fast and furious: Tokyo drift','5');
