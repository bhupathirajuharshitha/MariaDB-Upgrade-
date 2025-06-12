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

# Check for the usage of the reserved word OFFSET
check_offset_usage() {
  echo "==================================================="
  echo "Checking for usage of the reserved word 'OFFSET' in names..."
  echo "---------------------------------------------------"
  echo "New reserved word: OFFSET. This can no longer be used as an identifier without being quoted."
  echo "---------------------------------------------------"
  
  MYSQL_CMD="mysql -h $HOSTNAME -u $USERNAME -p$PASSWORD -e"
  OFFSET_USAGE=$($MYSQL_CMD "SELECT table_name FROM information_schema.tables WHERE table_name LIKE '%offset%';" | tail -n +2)
  
  if [ -z "$OFFSET_USAGE" ]; then
    echo "No tables found using 'OFFSET' in their names."
  else
    echo "Tables using 'OFFSET' in their names:"
    echo "$OFFSET_USAGE"
  fi
  echo "==================================================="
}

# List all tables using COMPRESSED row format
list_compressed_tables() {
  echo "==================================================="
  echo "Listing tables with COMPRESSED row format..."
  echo "---------------------------------------------------"
  echo "From MariaDB 10.6.0 until MariaDB 10.6.5, tables that are of the COMPRESSED row format are read-only by default."
  echo "This was intended to be the first step towards removing write support and deprecating the feature."
  echo "---------------------------------------------------"
  echo "This plan has been scrapped, and from MariaDB 10.6.6, COMPRESSED tables are no longer read-only by default."
  echo "---------------------------------------------------"
  echo "From MariaDB 10.6.0 to MariaDB 10.6.5, set the innodb_read_only_compressed variable to OFF to make the tables writable."
  echo "---------------------------------------------------"
  
  MYSQL_CMD="mysql -h $HOSTNAME -u $USERNAME -p$PASSWORD -e"
  COMPRESSED_TABLES=$($MYSQL_CMD "SELECT table_name FROM information_schema.tables WHERE row_format = 'COMPRESSED';" | tail -n +2)
  
  if [ -z "$COMPRESSED_TABLES" ]; then
    echo "No tables found using COMPRESSED row format."
  else
    echo "COMPRESSED Tables:"
    echo "$COMPRESSED_TABLES"
  fi
  echo "==================================================="
}

# Check for changed default values
check_changed_defaults() {
  echo "==================================================="
  echo "Checking options with changed default values..."
  echo "---------------------------------------------------"

  MYSQL_CMD="mysql -h $HOSTNAME -u $USERNAME -p$PASSWORD -e"

  OPTIONS=(
    "character_set_client"
    "character_set_connection"
    "character_set_results"
    "character_set_system"
    "innodb_flush_method"
    "old_mode"
  )

  OLD_DEFAULTS=(
    "utf8"
    "utf8"
    "utf8"
    "utf8"
    "fsync"
    "Empty"
  )

  NEW_DEFAULTS=(
    "utf8mb3"
    "utf8mb3"
    "utf8mb3"
    "utf8mb3"
    "O_DIRECT"
    "UTF8_IS_UTF8MB3"
  )

  DESCRIPTIONS=(
    "Sets the client's character set to utf8mb3 by default."
    "Changes the connection's character set to utf8mb3."
    "Results are now utf8mb3 coded by default."
    "System character set set to utf8mb3 for backward compatibility."
    "Flush method switched to O_DIRECT for direct disk access."
    "Defines default character set behavior for utf8 aliases."
  )

  for i in "${!OPTIONS[@]}"; do
    CURRENT_VALUE=$($MYSQL_CMD "SHOW VARIABLES LIKE '${OPTIONS[i]}'" | grep "${OPTIONS[i]}" | awk '{print $2}')
    echo "${OPTIONS[i]}: Current Value: $CURRENT_VALUE"
    echo "Old Default: ${OLD_DEFAULTS[i]}, New Default: ${NEW_DEFAULTS[i]}"
    echo "Description: ${DESCRIPTIONS[i]}"
    echo "---------------------------------------------------"
  done
  echo "==================================================="
}

# List options that have been removed or renamed
list_removed_or_renamed_options() {
  echo "==================================================="
  echo "Listing options that have been removed or renamed..."
  echo "---------------------------------------------------"

  REMOVED_RENAMED_OPTIONS=(
    "innodb_adaptive_max_sleep_delay"
    "innodb_background_scrub_data_check_interval"
    "innodb_background_scrub_data_compressed"
    "innodb_background_scrub_data_interval"
    "innodb_background_scrub_data_uncompressed"
    "innodb_buffer_pool_instances"
    "innodb_checksum_algorithm: The variable is still present, but the *innodb and *none options have been removed."
    "innodb_commit_concurrency"
    "innodb_concurrency_tickets"
    "innodb_file_format"
    "innodb_large_prefix"
    "innodb_lock_schedule_algorithm"
    "innodb_log_checksums"
    "innodb_log_compressed_pages"
    "innodb_log_files_in_group"
    "innodb_log_optimize_ddl"
    "innodb_page_cleaners"
    "innodb_replication_delay"
    "innodb_scrub_log"
    "innodb_scrub_log_speed"
    "innodb_sync_array_size"
    "innodb_thread_concurrency"
    "innodb_thread_sleep_delay"
    "innodb_undo_logs"
  )

  DESCRIPTIONS_REMOVED=(
    "Obsolete performance tuning."
    "Removed for efficiency."
    "Not needed; focusing on core features."
    "Optimization technique deprecated."
    "Focused on advanced safety features only."
    "Dynamic resource handling without instances."
    "Reliance on crc32 algorithm from MariaDB 10.6 onward."
    "Simplifying concurrency handling."
    "Efficient ticket handling methods in place."
    "File format changes deprecated."
    "Unified prefix handling."
    "Scheduling improved without setting needed."
    "Log checksum handling optimized."
    "Compression strategy revised."
    "File management streamlined."
    "DDL optimization managed internally."
    "Cleaner strategy adjusted."
    "Replication managed through other means."
    "Log scrubbing strategy deprecated."
    "Scrubbing speed internalized."
    "Sync array optimized internally."
    "Thread handling streamlined."
    "Delay strategy no longer needed."
    "Undo log strategy updated."
  )

  for i in "${!REMOVED_RENAMED_OPTIONS[@]}"; do
    echo "${REMOVED_RENAMED_OPTIONS[i]}"
    echo "Description: ${DESCRIPTIONS_REMOVED[i]}"
    echo "---------------------------------------------------"
  done
  echo "==================================================="
}

# List deprecated options
list_deprecated_options() {
  echo "==================================================="
  echo "Listing deprecated options and their reasons..."
  echo "---------------------------------------------------"

  DEPRECATED_OPTIONS=(
    "wsrep_replicate_myisam: Use wsrep_mode instead."
    "wsrep_strict_ddl: Use wsrep_mode instead."
  )

  DESCRIPTIONS_DEPRECATED=(
    "MyISAM replication replaced by wsrep_mode."
    "Strict DDL checks managed by wsrep_mode instead."
  )

  for i in "${!DEPRECATED_OPTIONS[@]}"; do
    echo "${DEPRECATED_OPTIONS[i]}"
    echo "Description: ${DESCRIPTIONS_DEPRECATED[i]}"
    echo "---------------------------------------------------"
  done
  echo "==================================================="
}

# Main script execution
read_db_credentials
check_offset_usage
list_compressed_tables
check_changed_defaults
list_removed_or_renamed_options
list_deprecated_options
