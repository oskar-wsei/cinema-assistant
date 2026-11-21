import * as path from 'node:path';
import * as swagger from 'swagger-typescript-api';

const basePath = path.dirname(__filename);
const outputPath = path.join(basePath, '../src/app/types');
const outputName = 'api.types.ts';
const openApiUrl = 'http://localhost:8000/openapi.json';

async function main(): Promise<void> {
  console.log(`Generating API client from OpenAPI spec at ${openApiUrl} to ${outputPath}`);

  await swagger.generateApi({
    url: openApiUrl,
    output: outputPath,
    fileName: outputName,
    generateClient: false,
    extractEnums: true,
    extractRequestParams: true,
    enumStyle: 'union',
    extractingOptions: {
      enumSuffix: [''],
    },
  });
}

void main();
