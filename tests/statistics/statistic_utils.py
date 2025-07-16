import os
import pandas as pd


def copy_missing_values(main_file, copy_file, target_file, index_cols, columns_to_copy):
    main_df = pd.read_csv(main_file, sep='\t', dtype=str)
    copy_df = pd.read_csv(copy_file, sep='\t', dtype=str)

    # Create concatenated index
    main_df['concat_index'] = main_df[index_cols[0]].astype(str) + '|' + main_df[index_cols[1]].astype(str)
    copy_df['concat_index'] = copy_df[index_cols[0]].astype(str) + '|' + copy_df[index_cols[1]].astype(str)
    main_df = main_df.set_index('concat_index')
    copy_df = copy_df.set_index('concat_index')

    for col in columns_to_copy:
        for idx in main_df.index:
            main_val = main_df.loc[idx, col] if col in main_df.columns else None
            copy_val = copy_df.loc[idx, col] if (col in copy_df.columns and idx in copy_df.index) else None
            if is_empty(main_val):
                if not is_empty(copy_val):
                    main_df.loc[idx, col] = copy_val
            else:
                if not is_empty(copy_val):
                    print(
                        f'Row {idx}, column {col}: main value not empty ("{main_val}"), copy value ("{copy_val}") not copied.')

    # Reset index and drop the concat_index column before saving
    main_df = main_df.reset_index()
    main_df.to_csv(target_file, sep='\t', index=False)

def is_empty(val):
    if pd.isna(val):
        return True
    if isinstance(val, str) and val.strip().lower() in ['', 'nan']:
        return True
    return False

if __name__ == "__main__":
    current_folder = os.path.dirname(os.path.abspath(__file__))
    main_file = os.path.join(current_folder, '../test_data/cell_type_validation_report.tsv')
    copy_file = os.path.join(current_folder, '../test_data/LLM_False_assertions.tsv')
    target_file = os.path.join(current_folder, '../test_data/cell_type_validation_report_2.tsv')
    copy_missing_values(main_file, copy_file, target_file, ["Cell ID", "Assertion"], ["Curator Validation"])