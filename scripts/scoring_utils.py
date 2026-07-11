def get_max_score(r):
    """
    Computes the maximum possible score for a sample.
    If text_completeness is N/A, the max score is 5.
    Otherwise, it is 6.
    Even if pipeline_status is 'not_run', it counts out of 6 (Option B methodology).
    """
    possible = 6
    if str(r.get('text_completeness')) == 'N/A':
        possible -= 1
    return possible

def get_score(r):
    """
    Computes the earned score for a sample (Option B methodology).
    If it fails to compile or pipeline_status is not_run, it scores 0.
    """
    if r.get('compiles', 0) == 0 or r.get('pipeline_status', 'ran') == 'not_run' or r.get('pipeline_status', 'ran') == 'extraction_failed':
        return 0
        
    earned = (r.get('compiles', 0) + 
              r.get('no_leaked_source', 0) + 
              r.get('structural_elements', 0) + 
              r.get('numbering_correctness', 0) + 
              r.get('typography_correctness', 0))
              
    if str(r.get('text_completeness')) != 'N/A':
        earned += r.get('text_completeness', 0)
        
    return earned

def compute_average(records):
    """
    Enforces Option B: Total earned across all records / total possible.
    Includes not_run and failures in the denominator.
    Returns the average scaled to 6.0.
    """
    total_earned = sum([get_score(r) for r in records])
    total_possible = sum([get_max_score(r) for r in records])
    if total_possible == 0:
        return 0.0
    return (total_earned / total_possible) * 6.0

def get_patched_ceiling_records(all_records, engine_name):
    """
    Blends patched records with baseline records correctly.
    If a patched variant exists for a sample, use it.
    Otherwise, fall back to the baseline record for that engine.
    This guarantees exactly 48 records per engine without double counting.
    """
    patched_records = []
    
    # 1. Get all base records for this engine
    base_records = [r for r in all_records if r.get('candidate') == engine_name]
    
    # 2. Build a map of sample_id -> patched record for this engine
    # A record is the patched version of this engine if it is_patched and starts with engine_name
    patched_map = {r.get('sample_id'): r for r in all_records if r.get('is_patched', False) and r.get('candidate', '').startswith(engine_name)}
    
    # 3. Iterate through base records. If a patched variant exists, use it. Else use base.
    for br in base_records:
        sample_id = br.get('sample_id')
        if sample_id in patched_map:
            patched_records.append(patched_map[sample_id])
        else:
            patched_records.append(br)
            
    return patched_records

def get_pass_rate(records, metric):
    """
    Computes pass rate for a single metric across records.
    Excludes N/A fields from the denominator.
    """
    if not records: return 0.0
    passed = 0
    total = 0
    for r in records:
        if str(r.get(metric)) == 'N/A': continue
        total += 1
        # Hard failure on compilation or pipeline failure cascades to 0
        if r.get('compiles', 0) == 0 and metric != 'compiles': continue
        if r.get('pipeline_status', 'ran') in ['not_run', 'extraction_failed'] and metric != 'compiles': continue
        if r.get(metric) == 1: passed += 1
    if total == 0: return 0.0
    return (passed / total) * 100
