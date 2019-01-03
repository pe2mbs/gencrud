insert into WA_ROLES ( D_ROLE_NAME ) values ( 'Administrator' );
insert into WA_ROLES ( D_ROLE_NAME ) values ( 'Test Manager' );
insert into WA_ROLES ( D_ROLE_NAME ) values ( 'Test QA' );
insert into WA_ROLES ( D_ROLE_NAME ) values ( 'Test Analist' );
insert into WA_ROLES ( D_ROLE_NAME ) values ( 'Test Engineer' );
insert into WA_ROLES ( D_ROLE_NAME ) values ( 'Tester' );

insert into WA_USERS ( D_USER_NAME, D_PASSWORD, D_FIRST_NAME, D_MIDDLE_NAME, D_LAST_NAME, D_ROLE_ID, D_LAST_CHANGED )
       values ( 'mbertens', '5701mb', 'Marc', '', 'Bertens-Nguyen', 1, DateTime('now', 'UTC') );

insert into WA_USERS ( D_USER_NAME, D_PASSWORD, D_FIRST_NAME, D_MIDDLE_NAME, D_LAST_NAME, D_ROLE_ID, D_LAST_CHANGED )
       values ( 'erijerse', '123456', 'Ernst', '', 'Rijerse', 1, DateTime('now', 'localtime') );


insert into WA_TESTER ( D_USER_NAME, D_PASSWORD, D_FIRST_NAME, D_MIDDLE_NAME, D_LAST_NAME, D_LAST_CHANGED )
       values ( 'mbertens', '5701mb', 'Marc', '', 'Bertens-Nguyen', DateTime('now', 'UTC') );

insert into WA_TESTER ( D_USER_NAME, D_PASSWORD, D_FIRST_NAME, D_MIDDLE_NAME, D_LAST_NAME, D_LAST_CHANGED )
       values ( 'erijerse', '123456', 'Ernst', '', 'Rijerse', DateTime('now', 'localtime') );



