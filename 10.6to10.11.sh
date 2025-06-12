#!/bin/bash

# Function to prompt and read inputs without echoing password
read_db_credentials() {
  echo -n "Enter MariaDB Hostname: "
  read HOSTNAME

  echo -n "Enter MariaDB Username: "
  read USERNAME

  echo -n "Enter MariaDB Password: "
  read -s PASSWORD
  echo
}

# Check for changed default values
check_changed_defaults() {
  echo "Checking options with changed default values..."

  MYSQL_CMD="mysql -h $HOSTNAME -u $USERNAME -p$PASSWORD -e"

  OPTIONS=(
    "innodb_buffer_pool_chunk_size"
    "spider_auto_increment_mode"
    "spider_bgs_first_read"
    "spider_bgs_mode"
    "spider_bgs_second_read"
    "spider_bka_mode"
    "spider_bka_table_name_type"
    "spider_buffer_size"
    "spider_bulk_size"
    "spider_bulk_update_mode"
    "spider_bulk_update_size"
    "spider_casual_read"
    "spider_connect_timeout"
    "spider_crd_bg_mode"
    "spider_crd_interval"
    "spider_crd_mode"
    "spider_crd_sync"
    "spider_crd_type"
    "spider_crd_weight"
    "spider_delete_all_rows_type"
    "spider_direct_dup_insert"
    "spider_direct_order_limit"
    "spider_error_read_mode"
    "spider_error_write_mode"
    "spider_first_read"
    "spider_init_sql_alloc_size"
    "spider_internal_limit"
    "spider_internal_offset"
    "spider_internal_optimize"
    "spider_internal_optimize_local"
    "spider_load_crd_at_startup"
    "spider_load_sts_at_startup"
    "spider_low_mem_read"
    "spider_max_order"
    "spider_multi_split_read"
    "spider_net_read_timeout"
    "spider_net_write_timeout"
    "spider_quick_mode"
    "spider_quick_page_byte"
    "spider_quick_page_size"
    "spider_read_only_mode"
    "spider_reset_sql_alloc"
    "spider_second_read"
    "spider_selupd_lock_mode"
    "spider_semi_split_read"
    "spider_semi_split_read_limit"
    "spider_semi_table_lock_connection"
    "spider_semi_table_lock"
  )

  OLD_DEFAULTS=(
    "134217728"
    "-1"
    "-1"
    "-1"
    "-1"
    "-1"
    "-1"
    "-1"
    "-1"
    "-1"
    "-1"
    "-1"
    "-1"
    "-1"
    "-1"
    "-1"
    "-1"
    "-1"
    "-1"
    "-1"
    "-1"
    "-1"
    "-1"
    "-1"
    "-1"
    "-1"
    "-1"
    "-1"
    "-1"
    "-1"
    "-1"
    "-1"
    "-1"
    "-1"
    "-1"
    "-1"
    "-1"
    "-1"
    "-1"
    "-1"
    "-1"
    "-1"
    "-1"
    "-1"
    "1"
  )

  NEW_DEFAULTS=(
    "Autosized"
    "0"
    "2"
    "0"
    "100"
    "1"
    "1"
    "16000"
    "16000"
    "0"
    "16000"
    "0"
    "6"
    "2"
    "51"
    "1"
    "0"
    "2"
    "2"
    "1"
    "0"
    "9223372036854775807"
    "0"
    "0"
    "0"
    "1024"
    "9223372036854775807"
    "0"
    "0"
    "0"
    "1"
    "1"
    "1"
    "32767"
    "100"
    "600"
    "600"
    "3"
    "10485760"
    "1024"
    "0"
    "1"
    "0"
    "1"
    "2"
    "1"
    "1"
    "0"
  )

  DESCRIPTIONS=(
    "Controls size of memory chunks allocated to the InnoDB buffer pool, now autosized for optimization."
    "Sets behavior for auto-increment columns; ensuring reliability."
    "Adjusts the batch reading strategy to enhance query performance under Spider engine."
    "Manages batch processing for Spider engine operations, improving speed."
    "Configures secondary batch read parameters for Spider to handle queries efficiently."
    "Determines mode for batch key access hence optimizing indexing."
    "Specifies how table names are processed in BKA, enabling better compatibility."
    "Defines buffer size for Spider operations, crucial for handling large data transfers."
    "Adjusts the bulk processing size for better handling of large payloads."
    "Sets mode for bulk update operations to facilitate batch changes."
    "Determines bulk update size for processing, enhancing batch update efficiency."
    "Optimizes casual read performance for Spider queries."
    "Adjusts timeout for connection attempts under Spider engine, enhancing reliability."
    "Configures background mode for CRD operations, improving asynchronous tasks."
    "Sets intervals for CRD processes, crucial for periodic updates."
    "Establishes mode for CRD operations, optimizing consistency."
    "Syncs CRD processes, ensuring data integrity."
    "Determines the processing type for CRD, enhancing data tasks."
    "Weights CRD procedure execution, allowing prioritization."
    "Defines types for deleting rows in Spider, optimizing space management."
    "Manages direct duplicate insert handling, reducing collision errors."
    "Limits direct ordering, enhancing result handling."
    "Sets error handling for read operations, ensuring robustness."
    "Defines error handling mode for writes, ensuring reliability."
    "Configures initial parameters for single read operations, improving efficiency."
    "Specifies allocation size for SQL initialization, optimizing setup."
    "Establishes limits for internal Spider operations, handling large results."
    "Adjusts internal offset strategies for Spider, improving query handling."
    "Optimizes internal Spider behaviors for better local execution."
    "Helps optimize local data handling during Spider queries."
    "Ensures CRD data is loaded at startup for prompt readiness."
    "Ensures stateful data (STS) loads for Spider operations during startup."
    "Improves memory efficiency for Spider reads, optimizing resource usage."
    "Sets max order processing volume for Spider, high-performant configurations."
    "Optimizes split reading processes in multi-node Spider setups."
    "Determines network read timeout for Spider transactions, critical for reliability."
    "Adjusts network write timeout settings under Spider, enhancing stability."
    "Optimizes quick mode for transferring Spider data rapidly."
    "Defines byte size for quick processing pages, customizing efficiency."
    "Decides page size for Spider queries, optimizing storage."
    "Configures read-only mode under Spider, restricting write operations."
    "Resets SQL allocation, tailoring query resource usage."
    "Controls secondary read setups for Spider, streamlining access."
    "Adjusts locking strategies, maintaining data integrity."
    "Optimizes semi-split reads, balancing resource utilization."
    "Defines limit for semi-split tasks, optimizing splits."
    "Manages lock connections for semi-table access, ensuring order."
    "Adjusts locking strategies under Spider, promoting concurrency."
  )

  for i in "${!OPTIONS[@]}"; do
    CURRENT_VALUE=$($MYSQL_CMD "SHOW VARIABLES LIKE '${OPTIONS[i]}'" | grep "${OPTIONS[i]}" | awk '{print $2}')
    echo "${OPTIONS[i]}: Current Value: $CURRENT_VALUE, Old Default: ${OLD_DEFAULTS[i]}, New Default: ${NEW_DEFAULTS[i]}"
    echo "Description: ${DESCRIPTIONS[i]}"
  done
}

# List options that have been removed or renamed
list_removed_or_renamed_options() {
  echo "Listing options that have been removed or renamed..."

  REMOVED_RENAMED_OPTIONS=(
    "innodb_log_write_ahead_size: On Linux and Windows, the physical block size of the underlying storage is instead detected and used."
    "innodb_version: Redundant."
    "wsrep_replicate_myisam: Use wsrep_mode instead."
  )

  for option in "${REMOVED_RENAMED_OPTIONS[@]}"; do
    echo "$option"
  done
}

# List deprecated options
list_deprecated_options() {
  echo "Listing deprecated options and their reasons..."

  DEPRECATED_OPTIONS=(
    "keep_files_on_create: MariaDB now deletes orphan files, so this setting should never be necessary."
  )

  for option in "${DEPRECATED_OPTIONS[@]}"; do
    echo "$option"
  done
}

# Main script execution
read_db_credentials
check_changed_defaults
list_removed_or_renamed_options
list_deprecated_options
