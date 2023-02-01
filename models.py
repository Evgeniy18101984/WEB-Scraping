from datetime import datetime
from sqlalchemy import MetaData, Table, String, Integer, Column, Float, DateTime

metadata = MetaData()


Laptops = Table(
    "Laptops",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("url", String, nullable=False),
    Column("visited_at", DateTime, default=datetime.now()),
    Column("product_name", String, nullable=False),
    Column("cpu_hhz", Float, nullable=False),
    Column("ram_gb", Integer, nullable=False),
    Column("ssd_gb", Integer, nullable=False),
    Column("price", Integer, nullable=False),
    Column("rank", Float, nullable=False),
)