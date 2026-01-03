from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        # This line ensures the product_id column exists before we try to use it
        ('core', '0003_cartorderitems_product'), 
    ]

    operations = [
        migrations.RunSQL(
            """
            -- REPLACING the old function with the FIXED logic
            CREATE OR REPLACE FUNCTION update_product_stock()
            RETURNS TRIGGER AS $$
            BEGIN
                UPDATE core_product
                -- Subtract stock from the specific product identified by product_id
                SET stock_count = stock_count - NEW.qty
                WHERE id = NEW.product_id;
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
            """
        )
    ]