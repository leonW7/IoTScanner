Create table info
(
    product_detail_url  varchar(200),
    vendor              varchar(20),
    source_              varchar(50),

    adapter             varchar(50),
    version             varchar(50),
    size                varchar(50),
    release_time        varchar(30),
    version_description text,


    url                 varchar(200),
    filename            varchar(100),
    checksum            varchar(32) primary key not null

)
