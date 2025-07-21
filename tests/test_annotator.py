from cellsem_agent.agents.paper_celltype.paper_celltype_tools import get_full_text


def test_foo():
    full_text = get_full_text(None, "./test_data/cell_mappings_input/gut/Burclaff_et_al._(2022)_paper.pdf")
    print(full_text)
    # assert foo("foo") == "foo"
