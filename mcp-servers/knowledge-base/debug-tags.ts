import * as edgedb from 'edgedb';

async function debug() {
  const client = edgedb.createClient({
    dsn: process.env.EDGEDB_DSN || 'edgedb://edgedb@localhost:5656/edgedb',
    tlsSecurity: 'insecure'
  });

  console.log('=== Tags in DB ===');
  const tags = await client.query('SELECT Tag { id, name, category } ORDER BY .name');
  console.log(JSON.stringify(tags, null, 2));

  console.log('\n=== Experiences with tags ===');
  const exp = await client.query('SELECT Experience { id, title, tags: { id, name } }');
  console.log(JSON.stringify(exp, null, 2));

  await client.close();
}

debug().catch(console.error);
