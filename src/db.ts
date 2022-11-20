import { Pool, Client } from "pg"

const connectionString = process.env.DATABASE_URL

export const pool = new Pool({connectionString})
