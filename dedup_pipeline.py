from hash_bridge import HashBridge

if __name__ == "__main__":
    dedup_store = HashBridge()

    duplicate_playbook_stream = [
        "Playbook 44: Restrict SSH root logins and switch listening interfaces.",
        "Playbook 44: Restrict SSH root logins and switch listening interfaces.", # Direct duplicate payload
        "Playbook 99: Purge application system buffer maps across execution targets."
    ]

    print("=== SECUREHASH-RAG LOG IDENTIFIER AND DEDUPLICATOR ===")
    
    for idx, playbook in enumerate(duplicate_playbook_stream):
        allocated_doc_id = 200 + idx
        status = dedup_store.process_and_deduplicate(playbook, allocated_doc_id)
        
        if status == -1:
            print(f"[NEW STORAGE ALLOCATION]: Document ID {allocated_doc_id} successfully mapped to knowledge store entries.")
        else:
            print(f"[!] DEDUPLICATION INTERCEPT: Duplicate detected. Content matches existing document reference: ID {status}")
