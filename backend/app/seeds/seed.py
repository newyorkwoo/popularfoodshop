"""Seed runner"""
from app.seeds import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())
