from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
     
        ('core', '0004_fix_stock_trigger'), 
    ]

    operations = [
        migrations.RunSQL(
            """
            -- REPLACING the function with VALIDATION logic
            CREATE OR REPLACE FUNCTION update_product_stock()
            RETURNS TRIGGER AS $$
            DECLARE
                current_stock integer;
            BEGIN
                -- Get the current stock of the product being ordered
                SELECT stock_count INTO current_stock 
                FROM core_product 
                WHERE id = NEW.product_id;

                -- 1. Validation: Check if stock exists
                IF current_stock IS NULL THEN
                    RAISE EXCEPTION 'Product ID % not found', NEW.product_id;
                END IF;

                -- 2. Validation: Prevent negative stock (Overselling)
                IF current_stock < NEW.qty THEN
                    RAISE EXCEPTION 'Insufficient stock for Product %. Have: %, Requested: %', NEW.product_id, current_stock, NEW.qty;
                END IF;

                -- 3. Execution: If checks pass, update the stock
                UPDATE core_product
                SET stock_count = stock_count - NEW.qty
                WHERE id = NEW.product_id;

                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
            """
        )
    ]