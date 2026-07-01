#ifndef DEDUP_HASH_H
#define DEDUP_HASH_H

typedef struct HashEntry HashEntry;
typedef struct DedupTable DedupTable;
DedupTable* init_table();
int register_document_payload(DedupTable* dt, const char* text_hash, int doc_id);
void clear_table(DedupTable* dt);

#endif
