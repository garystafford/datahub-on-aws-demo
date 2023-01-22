-- tickit_rev.fct_revenue
comment on table
"tickit_rev"."fct_revenue" is 'Tickit Database Revenue Fact Table. Each row represents a sale of one or more tickets for a specific event, as offered in a specific listing.';

comment on column
"tickit_rev"."fct_revenue"."salesid" is 'Primary key, a unique ID value for each row. Each row represents a sale of one or more tickets for a specific event, as offered in a specific listing.';

comment on column
"tickit_rev"."fct_revenue"."dateid" is 'Foreign-key reference to the DATE table.';

comment on column
"tickit_rev"."fct_revenue"."eventid" is 'Foreign-key reference to the EVENT table.';

comment on column
"tickit_rev"."fct_revenue"."venueid" is 'Foreign-key reference to the VENUE table.';

comment on column
"tickit_rev"."fct_revenue"."catid" is 'Foreign-key reference to the CATEGORY table.';

comment on column
"tickit_rev"."fct_revenue"."pricepaid" is 'The total price paid for the tickets, such as 75.00 or 488.00. The individual price of a ticket is PRICEPAID/QTYSOLD.';

comment on column
"tickit_rev"."fct_revenue"."commission" is 'The 15% commission that the business collects from the sale, such as 11.25 or 73.20. The seller receives 85% of the PRICEPAID value.';

-- tickit_rev.dim_venue
comment on table
"tickit_rev"."dim_venue" is 'Tickit Database Venue Dimension Table. Each row represents a specific venue where events take place.';

comment on column
"tickit_rev"."dim_venue"."venueid" is 'Primary key, a unique ID value for each row. Each row represents a specific venue where events take place.';

comment on column
"tickit_rev"."dim_venue"."venuename" is 'Exact name of the venue, such as Cleveland Browns Stadium.';
