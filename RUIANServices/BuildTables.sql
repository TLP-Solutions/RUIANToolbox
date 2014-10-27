drop table if exists typ_st_objektu;
CREATE TABLE typ_st_objektu
(
  kod integer NOT NULL,
  nazev character varying NOT NULL,
  popis character varying,
  zkratka character varying,
  CONSTRAINT typ_st_objektu_pkey PRIMARY KEY (kod)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE typ_st_objektu
  OWNER TO postgres;

INSERT INTO typ_st_objektu VALUES (1,'Budova s číslem popisným','Budova s číslem popisným','č.p.');
INSERT INTO typ_st_objektu VALUES (2,'Budova s číslem evidenčním','Budova s číslem evidenčním','č.ev.');
INSERT INTO typ_st_objektu VALUES (3,'Budova bez č.p. a č.ev.','Budova bez čísla popisného a bez čísla evidenčního','');

drop table if exists ui_momc;
CREATE TABLE ui_momc
(
  kod integer,
  nazev character varying,
  obec_kod integer,
  mop_kod character varying,
  spravobv_kod character varying,
  poradi integer
)
WITH (
  OIDS=FALSE
);
ALTER TABLE ui_momc
  OWNER TO postgres;
  
INSERT INTO ui_momc VALUES (551082,'Brno-Bohunice',582786,'','',1);
INSERT INTO ui_momc VALUES (551325,'Brno-Bosonohy',582786,'','',2);
INSERT INTO ui_momc VALUES (551198,'Brno-Bystrc',582786,'','',3);
INSERT INTO ui_momc VALUES (551317,'Brno-Chrlice',582786,'','',5);
INSERT INTO ui_momc VALUES (551376,'Brno-Ivanovice',582786,'','',6);
INSERT INTO ui_momc VALUES (551406,'Brno-Jehnice',582786,'','',7);
INSERT INTO ui_momc VALUES (551171,'Brno-Jundrov',582786,'','',9);
INSERT INTO ui_momc VALUES (551210,'Brno-Kníničky',582786,'','',10);
INSERT INTO ui_momc VALUES (551147,'Brno-Kohoutovice',582786,'','',11);
INSERT INTO ui_momc VALUES (551228,'Brno-Komín',582786,'','',12);
INSERT INTO ui_momc VALUES (551007,'Brno-Královo Pole',582786,'','',13);
INSERT INTO ui_momc VALUES (551287,'Brno-Líšeň',582786,'','',14);
INSERT INTO ui_momc VALUES (551252,'Brno-Maloměřice a Obřany',582786,'','',15);
INSERT INTO ui_momc VALUES (551236,'Brno-Medlánky',582786,'','',16);
INSERT INTO ui_momc VALUES (551112,'Brno-Nový Lískovec',582786,'','',17);
INSERT INTO ui_momc VALUES (551422,'Brno-Ořešín',582786,'','',18);
INSERT INTO ui_momc VALUES (551295,'Brno-Slatina',582786,'','',21);
INSERT INTO ui_momc VALUES (551091,'Brno-Starý Lískovec',582786,'','',22);
INSERT INTO ui_momc VALUES (551309,'Brno-Tuřany',582786,'','',24);
INSERT INTO ui_momc VALUES (551279,'Brno-Vinohrady',582786,'','',26);
INSERT INTO ui_momc VALUES (551074,'Brno-jih',582786,'','',8);
INSERT INTO ui_momc VALUES (551031,'Brno-sever',582786,'','',20);
INSERT INTO ui_momc VALUES (550973,'Brno-střed',582786,'','',23);
INSERT INTO ui_momc VALUES (550990,'Brno-Žabovřesky',582786,'','',27);
INSERT INTO ui_momc VALUES (551368,'Brno-Žebětín',582786,'','',28);
INSERT INTO ui_momc VALUES (551058,'Brno-Židenice',582786,'','',29);
INSERT INTO ui_momc VALUES (551066,'Brno-Černovice',582786,'','',4);
INSERT INTO ui_momc VALUES (551244,'Brno-Řečkovice a Mokrá Hora',582786,'','',19);
INSERT INTO ui_momc VALUES (551431,'Brno-Útěchov',582786,'','',25);
INSERT INTO ui_momc VALUES (554332,'Hošťálkovice',554821,'','',1);
INSERT INTO ui_momc VALUES (554669,'Hrabová',554821,'','',2);
INSERT INTO ui_momc VALUES (555355,'Komárov',505927,'','',1);
INSERT INTO ui_momc VALUES (554561,'Krásné Pole',554821,'','',3);
INSERT INTO ui_momc VALUES (554324,'Lhotka',554821,'','',4);
INSERT INTO ui_momc VALUES (556904,'Liberec (nečleněné město)',563889,'','',0);
INSERT INTO ui_momc VALUES (556891,'Liberec-Vratislavice nad Nisou',563889,'','',1);
INSERT INTO ui_momc VALUES (555339,'Malé Hoštice',505927,'','',2);
INSERT INTO ui_momc VALUES (554286,'Mariánské Hory a Hulváky',554821,'','',5);
INSERT INTO ui_momc VALUES (554570,'Martinov',554821,'','',6);
INSERT INTO ui_momc VALUES (554430,'Michálkovice',554821,'','',7);
INSERT INTO ui_momc VALUES (555436,'Milostovice',505927,'','',3);
INSERT INTO ui_momc VALUES (545911,'Moravská Ostrava a Přívoz',554821,'','',8);
INSERT INTO ui_momc VALUES (554219,'Nová Bělá',554821,'','',9);
INSERT INTO ui_momc VALUES (554367,'Nová Ves',554821,'','',10);
INSERT INTO ui_momc VALUES (555321,'Opava (nečleněná část města)',505927,'','',0);
INSERT INTO ui_momc VALUES (546135,'Ostrava-Jih',554821,'','',11);
INSERT INTO ui_momc VALUES (574716,'Pardubice I',555134,'','',1);
INSERT INTO ui_momc VALUES (555126,'Pardubice II',555134,'','',2);
INSERT INTO ui_momc VALUES (557064,'Pardubice III',555134,'','',3);
INSERT INTO ui_momc VALUES (555096,'Pardubice IV',555134,'','',4);
INSERT INTO ui_momc VALUES (557072,'Pardubice V',555134,'','',5);
INSERT INTO ui_momc VALUES (555100,'Pardubice VI',555134,'','',6);
INSERT INTO ui_momc VALUES (555118,'Pardubice VII',555134,'','',7);
INSERT INTO ui_momc VALUES (575020,'Pardubice VIII',555134,'','',8);
INSERT INTO ui_momc VALUES (554308,'Petřkovice',554821,'','',12);
INSERT INTO ui_momc VALUES (554723,'Plesná',554821,'','',13);
INSERT INTO ui_momc VALUES (545970,'Plzeň 1',554791,'','',1);
INSERT INTO ui_momc VALUES (557978,'Plzeň 10-Lhota',554791,'','',10);
INSERT INTO ui_momc VALUES (545988,'Plzeň 2-Slovany',554791,'','',2);
INSERT INTO ui_momc VALUES (546003,'Plzeň 3',554791,'','',3);
INSERT INTO ui_momc VALUES (546208,'Plzeň 4',554791,'','',4);
INSERT INTO ui_momc VALUES (554731,'Plzeň 5-Křimice',554791,'','',5);
INSERT INTO ui_momc VALUES (554758,'Plzeň 6-Litice',554791,'','',6);
INSERT INTO ui_momc VALUES (554766,'Plzeň 7-Radčice',554791,'','',7);
INSERT INTO ui_momc VALUES (554774,'Plzeň 8-Černice',554791,'','',8);
INSERT INTO ui_momc VALUES (559199,'Plzeň 9-Malesice',554791,'','',9);
INSERT INTO ui_momc VALUES (555401,'Podvihov',505927,'','',4);
INSERT INTO ui_momc VALUES (554588,'Polanka nad Odrou',554821,'','',14);
INSERT INTO ui_momc VALUES (546224,'Poruba',554821,'','',15);
INSERT INTO ui_momc VALUES (500054,'Praha 1',554782,'19','19',1);
INSERT INTO ui_momc VALUES (500224,'Praha 10',554782,'108','108',10);
INSERT INTO ui_momc VALUES (547034,'Praha 11',554782,'43','116',11);
INSERT INTO ui_momc VALUES (547107,'Praha 12',554782,'43','124',12);
INSERT INTO ui_momc VALUES (539694,'Praha 13',554782,'51','132',13);
INSERT INTO ui_momc VALUES (547361,'Praha 14',554782,'94','141',14);
INSERT INTO ui_momc VALUES (547387,'Praha 15',554782,'108','159',15);
INSERT INTO ui_momc VALUES (539601,'Praha 16',554782,'51','205',16);
INSERT INTO ui_momc VALUES (547174,'Praha 17',554782,'60','213',17);
INSERT INTO ui_momc VALUES (547417,'Praha 18',554782,'94','221',18);
INSERT INTO ui_momc VALUES (547344,'Praha 19',554782,'94','167',19);
INSERT INTO ui_momc VALUES (500089,'Praha 2',554782,'27','27',2);
INSERT INTO ui_momc VALUES (538213,'Praha 20',554782,'94','175',20);
INSERT INTO ui_momc VALUES (538949,'Praha 21',554782,'94','183',21);
INSERT INTO ui_momc VALUES (538931,'Praha 22',554782,'108','191',22);
INSERT INTO ui_momc VALUES (500097,'Praha 3',554782,'35','35',3);
INSERT INTO ui_momc VALUES (500119,'Praha 4',554782,'43','43',4);
INSERT INTO ui_momc VALUES (500143,'Praha 5',554782,'51','51',5);
INSERT INTO ui_momc VALUES (500178,'Praha 6',554782,'60','60',6);
INSERT INTO ui_momc VALUES (500186,'Praha 7',554782,'78','78',7);
INSERT INTO ui_momc VALUES (500208,'Praha 8',554782,'86','86',8);
INSERT INTO ui_momc VALUES (500216,'Praha 9',554782,'94','94',9);
INSERT INTO ui_momc VALUES (538078,'Praha-Benice',554782,'108','191',24);
INSERT INTO ui_momc VALUES (538060,'Praha-Běchovice',554782,'94','183',23);
INSERT INTO ui_momc VALUES (538124,'Praha-Březiněves',554782,'86','86',25);
INSERT INTO ui_momc VALUES (547301,'Praha-Dolní Chabry',554782,'86','86',28);
INSERT INTO ui_momc VALUES (547379,'Praha-Dolní Měcholupy',554782,'108','159',29);
INSERT INTO ui_momc VALUES (538175,'Praha-Dolní Počernice',554782,'94','141',30);
INSERT INTO ui_momc VALUES (538205,'Praha-Dubeč',554782,'108','159',31);
INSERT INTO ui_momc VALUES (538302,'Praha-Klánovice',554782,'94','183',32);
INSERT INTO ui_momc VALUES (538353,'Praha-Koloděje',554782,'94','183',33);
INSERT INTO ui_momc VALUES (538361,'Praha-Kolovraty',554782,'108','191',34);
INSERT INTO ui_momc VALUES (538388,'Praha-Královice',554782,'108','191',35);
INSERT INTO ui_momc VALUES (547042,'Praha-Kunratice',554782,'43','43',37);
INSERT INTO ui_momc VALUES (538400,'Praha-Křeslice',554782,'108','116',36);
INSERT INTO ui_momc VALUES (547051,'Praha-Libuš',554782,'43','124',38);
INSERT INTO ui_momc VALUES (539449,'Praha-Lipence',554782,'51','205',39);
INSERT INTO ui_momc VALUES (539465,'Praha-Lochkov',554782,'51','205',40);
INSERT INTO ui_momc VALUES (547140,'Praha-Lysolaje',554782,'60','60',41);
INSERT INTO ui_momc VALUES (547158,'Praha-Nebušice',554782,'60','60',42);
INSERT INTO ui_momc VALUES (538531,'Praha-Nedvězí',554782,'108','191',43);
INSERT INTO ui_momc VALUES (547395,'Praha-Petrovice',554782,'108','159',44);
INSERT INTO ui_momc VALUES (539589,'Praha-Přední Kopanina',554782,'60','60',45);
INSERT INTO ui_momc VALUES (538736,'Praha-Satalice',554782,'94','167',47);
INSERT INTO ui_momc VALUES (539678,'Praha-Slivenec',554782,'51','51',48);
INSERT INTO ui_momc VALUES (547271,'Praha-Suchdol',554782,'60','60',49);
INSERT INTO ui_momc VALUES (547328,'Praha-Troja',554782,'78','78',52);
INSERT INTO ui_momc VALUES (547115,'Praha-Velká Chuchle',554782,'51','205',54);
INSERT INTO ui_momc VALUES (539007,'Praha-Vinoř',554782,'94','167',55);
INSERT INTO ui_momc VALUES (539864,'Praha-Zbraslav',554782,'51','205',56);
INSERT INTO ui_momc VALUES (539899,'Praha-Zličín',554782,'51','213',57);
INSERT INTO ui_momc VALUES (539724,'Praha-Šeberov',554782,'43','116',50);
INSERT INTO ui_momc VALUES (547409,'Praha-Štěrboholy',554782,'108','159',51);
INSERT INTO ui_momc VALUES (547310,'Praha-Čakovice',554782,'94','221',26);
INSERT INTO ui_momc VALUES (547298,'Praha-Ďáblice',554782,'86','86',27);
INSERT INTO ui_momc VALUES (539635,'Praha-Řeporyje',554782,'51','132',46);
INSERT INTO ui_momc VALUES (539791,'Praha-Újezd',554782,'43','116',53);
INSERT INTO ui_momc VALUES (554375,'Proskovice',554821,'','',16);
INSERT INTO ui_momc VALUES (554243,'Pustkovec',554821,'','',17);
INSERT INTO ui_momc VALUES (554537,'Radvanice a Bartovice',554821,'','',18);
INSERT INTO ui_momc VALUES (546046,'Slezská Ostrava',554821,'','',19);
INSERT INTO ui_momc VALUES (554235,'Stará Bělá',554821,'','',20);
INSERT INTO ui_momc VALUES (555371,'Suché Lazce',505927,'','',5);
INSERT INTO ui_momc VALUES (554685,'Svinov',554821,'','',21);
INSERT INTO ui_momc VALUES (554715,'Třebovice',554821,'','',22);
INSERT INTO ui_momc VALUES (555461,'Vlaštovičky',505927,'','',7);
INSERT INTO ui_momc VALUES (556700,'Vávrovice',505927,'','',6);
INSERT INTO ui_momc VALUES (554227,'Vítkovice',554821,'','',23);
INSERT INTO ui_momc VALUES (555410,'Zlatníky',505927,'','',8);
INSERT INTO ui_momc VALUES (502081,'Ústí nad Labem-Neštěmice',554804,'','',2);
INSERT INTO ui_momc VALUES (501298,'Ústí nad Labem-Severní Terasa',554804,'','',3);
INSERT INTO ui_momc VALUES (502316,'Ústí nad Labem-Střekov',554804,'','',4);
INSERT INTO ui_momc VALUES (567892,'Ústí nad Labem-město',554804,'','',1);
  

drop table if exists ui_mop;
CREATE TABLE ui_mop
(
  kod character varying,
  nazev character varying,
  obec_kod integer
)
WITH (
  OIDS=FALSE
);
ALTER TABLE ui_mop
  OWNER TO postgres;
  
INSERT INTO ui_mop VALUES ('19','Praha 1',554782);
INSERT INTO ui_mop VALUES ('27','Praha 2',554782);
INSERT INTO ui_momc VALUES ('35','Praha 3',554782);
INSERT INTO ui_momc VALUES ('43','Praha 4',554782);
INSERT INTO ui_momc VALUES ('51','Praha 5',554782);
INSERT INTO ui_momc VALUES ('60','Praha 6',554782);
INSERT INTO ui_momc VALUES ('78','Praha 7',554782);
INSERT INTO ui_momc VALUES ('86','Praha 8',554782);
INSERT INTO ui_momc VALUES ('94','Praha 9',554782);
INSERT INTO ui_momc VALUES ('108','Praha 10',554782);

-- ##################################################
-- This script creates full text search tables
-- ##################################################

drop table if exists address_points;
CREATE TABLE address_points
AS SELECT adresnimista.kod gid, obce.kod kod_obce, obce.nazev nazev_obce, ui_momc.nazev nazev_momc, ui_mop.nazev nazev_mop, castiobci.kod kod_casti_obce, castiobci.nazev nazev_casti_obce, ulice.nazev nazev_ulice, typ_st_objektu.zkratka typ_so, adresnimista.cislodomovni cislo_domovni, adresnimista.cisloorientacni cislo_orientacni, adresnimista.cisloorientacnipismeno znak_cisla_orientacniho, adresnimista.psc psc, -ST_X(adresnibod) latitude, -ST_Y(adresnibod) longitude, adresnimista.platiod plati_od, adresnimista.adresnibod the_geom
FROM adresnimista
LEFT OUTER JOIN ulice on (adresnimista.ulicekod=ulice.kod)
LEFT OUTER JOIN stavebniobjekty on (adresnimista.stavebniobjektkod=stavebniobjekty.kod )
LEFT OUTER JOIN castiobci on (stavebniobjekty.castobcekod=castiobci.kod)
LEFT OUTER JOIN obce on (castiobci.obeckod=obce.kod)
LEFT OUTER JOIN typ_st_objektu on (stavebniobjekty.typstavebnihoobjektukod=typ_st_objektu.kod)
LEFT OUTER JOIN ui_momc on (stavebniobjekty.momckod=ui_momc.kod)
LEFT OUTER JOIN ui_mop on (ui_momc.mop_kod=ui_mop.kod);

ALTER TABLE address_points ADD PRIMARY KEY (gid);

select UpdateGeometrySRID('public', 'address_points', 'the_geom', 5514);

-- --------------------------------------------------
-- Create temporary table fulltext_a and fill it with partial data
-- --------------------------------------------------
drop table if exists fulltext_a;
create table fulltext_a
as
select gid, concat(nazev_obce, ',', nazev_casti_obce, ',', nazev_ulice) searchstr
from address_points
where nazev_obce <> nazev_casti_obce;

-- --------------------------------------------------
-- add rest of values
-- --------------------------------------------------
insert into fulltext_a 
select gid, concat(nazev_obce, ',', nazev_ulice) searchstr
from address_points
where nazev_obce = nazev_casti_obce;

-- --------------------------------------------------
-- Create table fulltext
-- --------------------------------------------------
DROP TABLE IF EXISTS fulltext;
create table fulltext
as
SELECT searchstr, array_agg(gid) gids
FROM fulltext_a
GROUP BY searchstr;

-- --------------------------------------------------
-- Drop temporary table fulltext_a
-- --------------------------------------------------
drop table fulltext_a;

-- --------------------------------------------------
-- Create search function explode_array
-- --------------------------------------------------
create or replace function explode_array(in_array anyarray) returns setof anyelement as
$$
    select ($1)[s] from generate_series(1,array_upper($1, 1)) as s;
$$
language sql immutable;

-- --------------------------------------------------
-- Create table gids
-- --------------------------------------------------
drop table if exists gids;
create table gids
as
select gid from address_points
group by gid order by gid;

-- ##################################################
-- This script creates Auto complete search tables
-- ##################################################

-- --------------------------------------------------
-- Create table psc
-- --------------------------------------------------
drop table if exists ac_psc;
create table ac_psc
as
select CAST(psc AS text), nazev_obce
from address_points
group by psc, nazev_obce;

-- --------------------------------------------------
-- Create table address_points
-- --------------------------------------------------
drop table if exists ac_obce;
create table ac_obce
as
select nazev_obce
from address_points
group by nazev_obce
order by nazev_obce;

-- --------------------------------------------------
-- Create table ac_ulice
-- --------------------------------------------------
drop table if exists ac_ulice;
create table ac_ulice
as
select nazev_ulice, nazev_obce, CAST(psc AS text) from address_points where nazev_ulice <> '' 
group by nazev_ulice, nazev_obce, psc order by nazev_ulice, nazev_obce, psc;

-- --------------------------------------------------
-- Create table ac_casti_obce
-- --------------------------------------------------
drop table if exists ac_casti_obce;
create table ac_casti_obce as
select nazev_casti_obce, nazev_obce
from address_points
group by nazev_casti_obce, nazev_obce
order by nazev_casti_obce, nazev_obce;

