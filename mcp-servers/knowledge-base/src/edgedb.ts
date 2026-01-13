/**
 * EdgeDB Client Configuration and Connection
 */
import { createClient, type Client } from 'edgedb';

export class EdgeDBClient {
  private client: Client | null = null;

  private static normalizeArgs(args?: Record<string, any>): Record<string, any> | undefined {
    if (!args) return undefined;
    return Object.keys(args).length > 0 ? args : undefined;
  }

  async connect(): Promise<void> {
    this.client = createClient({
      dsn: process.env.EDGEDB_DSN || 'edgedb://edgedb@localhost:5656/main',
      tlsSecurity: (process.env.EDGEDB_TLS_SECURITY as any) || 'insecure'
    });

    // Test connection
    const result = await this.client.query<number>('SELECT 1');
    console.log('EdgeDB connected:', result);
  }

  async disconnect(): Promise<void> {
    if (this.client) {
      await this.client.close();
      this.client = null;
    }
  }

  /**
   * Execute raw EdgeQL query
   */
  async query<T = unknown>(query: string, args?: Record<string, any>): Promise<T[]> {
    if (!this.client) {
      throw new Error('EdgeDB client not connected');
    }
    return this.client.query<T>(query, EdgeDBClient.normalizeArgs(args));
  }

  /**
   * Execute query expecting single result
   */
  async querySingle<T = unknown>(query: string, args?: Record<string, any>): Promise<T | null> {
    if (!this.client) {
      throw new Error('EdgeDB client not connected');
    }
    return this.client.querySingle<T>(query, EdgeDBClient.normalizeArgs(args));
  }

  /**
   * Get underlying EdgeDB client for advanced use
   */
  getClient(): Client {
    if (!this.client) {
      throw new Error('EdgeDB client not connected');
    }
    return this.client;
  }
}
