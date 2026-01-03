from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),  # Ensures tables exist before trigger is created
    ]

    operations = [
        migrations.RunSQL(
            # SQL to create the Function and Trigger
            """
            -- Function to update stock
            CREATE OR REPLACE FUNCTION update_product_stock()
            RETURNS TRIGGER AS $$
            BEGIN
                UPDATE core_product
                SET stock_count = stock_count - NEW.qty
                WHERE id = NEW.id;
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;

            -- Trigger that fires AFTER an item is inserted into CartOrderItems
            CREATE TRIGGER trigger_update_stock
            AFTER INSERT ON core_cartorderitems
            FOR EACH ROW
            EXECUTE FUNCTION update_product_stock();
            """,
            # SQL to delete them if we roll back
            """
            DROP TRIGGER IF EXISTS trigger_update_stock ON core_cartorderitems;
            DROP FUNCTION IF EXISTS update_product_stock;
            """
        )
    ]