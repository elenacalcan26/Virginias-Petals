INSERT INTO customer
    (email, first_name, last_name)
VALUES
    ('victoriaolteanu@gmail.com', 'Victoria', 'Olteanu'),
    ('alecudima@gmail.com', 'Dima', 'Alecu'),
    ('carinaangelica@yahoo.com', 'Carina', 'Angelica'),
    ('monicamanolache@yahoo.com', 'Monica', 'Manolache'),
    ('sergiunistor@gmail.com', 'Sergiu', 'Nistor');

INSERT INTO vendor
    (email, company_name, company_address, bank_account)
VALUES
    ('gioiaflowers@gmail.com', 'Gioia Flowers', 'Splaiul Independenței 2k, București 030099, Romania', 'RO91RXSKP8S3DZ4CUY1TUY55'),
    ('mayumiflowers@yahoo.com', 'Mayumi Flowers', 'Bulevardul Ferdinand I 130, București 021397, Romania', 'RO33PNNYM8RT77T6WJ0R55PO'),
    ('dorablooms@gmail.com', 'Dora Bloom', 'Strada Seneslav Voievod 67, București, Romania', 'RO25CMVT0JYXKZK2O006GX04'),
    ('mikulflorar@gmail.com', 'Mikflorar', 'Strada Tipografilor 11, București, Romania', 'RO94YVJE61L7L55BPBSU3WKS'),
    ('eviaflore@yahoo.com', 'Floraria Evia', 'Bulevardul Dinicu Golescu 7, București 010861, Romania', 'RO50AFGPE526TZ88705K5MO6');

INSERT INTO product_category
    (product_category_name)
VALUES
    ('anthurium'),
    ('areca'),
    ('azalee'),
    ('begonie'),
    ('bonsai'),
    ('calathea'),
    ('ciclama'),
    ('citrofortunella'),
    ('guzmania'),
    ('kalanchoe'),
    ('orhidee'),
    ('spatifilum'),
    ('trandafiri'),
    ('violeta'),
    ('yucca');

INSERT INTO product
    (vendor_id, product_category_id, product_name, description, price, availability)
VALUES
    (1, 1, 'Anthurium, sageata lui Cupidon', 'Anthurium, o planta cu o legenda aparte. Se spune ca zeul iubirii, Cupidon, folosea florile de anthurium drept sageti! De aceea, anthurium a ramas cunoscuta ca o planta a iubirii si a prieteniei.', 149, 'in stock'),
    (1, 2, 'Areca', 'Palmierul chinezesc (Chrysalidocarpus Areca) are pe langa rolul estetic deosebit si proprietatea de a elimina toate toxinele din aer, fiind totodata si foarte usor de intretinut! Frunzele acestei plante au un aspect gratios si este o planta mereu verde, fiind potrivita oricarui apartament sau spatiu de lucru.', 275, 'in stock'),
    (1, 3, 'Azalee rosie', 'In limbajul florilor, azaleea este simbolul echilibrului si al cumpatarii. O planta cu origini exotice, iubita in Asia Orientala, simbolizand, totodata, feminitatea', 169, 'in stock'),
    (1, 4, 'Begonie', 'Una dintre cele mai iubite plante din tara noastra, Begonia se gaseste in foarte multe culori si varietati. Desi este o floare destul de pretentioasa, daca primeste ingrijirea corespunzatoare, begonia infloreste pe tot parcursul anului!', 179, 'out of stock'),
    (2, 5, 'Bonsai intelept', 'Bonsaiul este cunoscut in intreaga lume ca fiind un arbore in miniatura. Deoarece tehnica obtinerii acestor bijuterii vegetale este straveche, sunt supranumiti si arborii intelepciunii.', 300, 'in stock'),
    (2, 8, 'Citrofortunella', 'Citrofortunella Mitis este un arbust originar din zonele mediteraneene, aducand astfel exoticul in casa, balconul sau gradina fiecaruia!', 390, 'in stock'),
    (2, 9, 'Guzmania exotica', 'O planta ornamentala foarte indragita, deosebita prin colorit si aspect! Guzmania se adapteaza foarte usor chiar si in spatii mai putin luminoase, avand grija sa se impuna cu frumusetea ei atipica: frunze lungi de un verde stralucitor, in mijlocul carora rasare o floare de dimensiuni mari.', 179, 'in stock'),
    (4, 10, 'Kalanchoe delicata', 'Kalanchoe (Calansoe) este o planta ce provine din Madagascar si Africa, fiind usor de intretinut, iar inflorirea ei se produce continuu.', 150, 'in stock'),
    (1, 11, 'Orhidee roz', 'Orhideea este una dintre cele mai iubite flori, asociata, de-a lungul timpului, cu cele mai puternice sentimente de afectiune.', 149, 'in stock'),
    (2, 11, 'Orhidee galbena', 'Orhideea aduna in florile sale cele mai sincere trairi, de la inocenta copilariei la pasiunea iubirii.', 129, 'out of stock'),
    (4, 11, 'Orhidee alba', 'Orhideea alba, unica prin eleganta sa, este cadoul ideal in orice situatie. Poti darui o orhidee alba pentru a exprima armonia, prietenia, afectiunea neconditionata, sau pentru a spune "imi pare rau"!', 175, 'in stock'),
    (5, 11, 'Orhidee Dendrobium', 'Dendrobium Nobile reprezinta simbolul elegantei desavarsite. Acest gen de orhidee este cunoscut pentru multitudinea de flori ce infloresc pe o singura tulpina. Florile ei sunt mici si delicate.', 249, 'in stock'),
    (5, 12, 'Mini trandafiri', 'Dacă iubești trandafirii, dar nu ai o grădină în care să îi crești, mini trandafirii Rosa Kordana sunt alegerea perfectă!', 149, 'in stock'),
    (5, 13, 'Violeta de Parma', 'Violeta de Parma (cunoscuta si drept violeta africana sau Saintpaulia) se numara printre cele mai populare plante cu flori pentru spatiile de interior si infloreste tot anul, o data la cateva luni.', 89, 'in stock');

INSERT INTO tag
    (tag_name)
VALUES
    ('business'),
    ('felicitare'),
    ('multumire'),
    ('nunta'),
    ('funerare'),
    ('imi pare rau'),
    ('aniversare'),
    ('botez'),
    ('petreceri'),
    ('romantice');

INSERT INTO product_tag
    (product_id, tag_id)
VALUES
    (1, 1),
    (1, 5),
    (1, 6),
    (2, 1),
    (2, 4),
    (2, 5),
    (2, 6),
    (2, 8),
    (3, 1),
    (3, 10),
    (4, 2),
    (5, 3),
    (5, 7),
    (5, 8),
    (6, 6),
    (6, 10),
    (7, 8),
    (7, 9),
    (8, 2),
    (9, 1),
    (9, 2),
    (9, 3),
    (9, 7),
    (9, 8),
    (9, 10),
    (10, 9),
    (11, 3),
    (11, 6),
    (12, 4),
    (12, 5),
    (13, 1),
    (13, 2),
    (14, 3),
    (14, 4),
    (14, 5),
    (14, 6),
    (14, 7),
    (14, 8),
    (14, 9),
    (14, 10);


INSERT INTO cart
    (customer_id, total_price)
VALUES
    (1, 3214),
    (2, 3447),
    (3, 9895),
    (4, 7620),
    (5, 1014),
    (1, 0);

INSERT INTO cart_product
    (cart_id, product_id, quantity)
VALUES
    (1, 1, 1),
    (1, 2, 5),
    (1, 3, 10),
    (2, 1, 3),
    (2, 5, 10),
    (3, 6, 13),
    (3, 7, 20),
    (3, 8, 1),
    (3, 9, 5),
    (3, 11, 2),
    (4, 2, 10),
    (4, 12, 10),
    (4, 13, 10),
    (4, 14, 10),
    (5, 1, 4),
    (5, 3, 1),
    (5, 12, 1);

INSERT INTO "order"
    (cart_id, order_date, total_price, shipping_address, customer_bank_account)
VALUES
    (1, '2023-04-25', 3234, 'Calea Mesteacănului nr. 862, bl. 36, ap. 3, Mun. Vlăhița, Vaslui, CP 437360', 'RO05AEQMO1T5862ATS75K43R');
