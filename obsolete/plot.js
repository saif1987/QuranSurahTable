(async () => {
    const Bokeh = await Bokeh.embed.embedItem;
    const surahData = await fetch('surah.json').then(response => response.json());
    const df = surahData;

    function assignSurahColor(row) {
        if (row.makki_madani === 'Makki') return '#90ee90';
        else if (row.makki_madani === 'Madani') return '#f08080';
        else return 'gray';
    }

    df.forEach(row => row.colors = assignSurahColor(row));

    const maxSurahsPerRow = 17;
    const overflowData = [];
    const mainData = [];

    const groups = [...new Set(df.map(item => item.group))];

    groups.forEach(group => {
        const groupDf = df.filter(item => item.group === group);
        const madaniSurahs = groupDf.filter(item => item.makki_madani === 'Madani');
        const makkiSurahs = groupDf.filter(item => item.makki_madani === 'Makki');

        const madaniCount = madaniSurahs.length;
        const makkiCount = makkiSurahs.length;

        if (madaniCount <= maxSurahsPerRow) {
            if (madaniCount + makkiCount <= maxSurahsPerRow) {
                mainData.push(...groupDf);
            } else {
                mainData.push(...madaniSurahs);
                const remainingMakki = maxSurahsPerRow - madaniCount;
                mainData.push(...makkiSurahs.slice(0, remainingMakki));
                overflowData.push(...makkiSurahs.slice(remainingMakki).map(item => ({ ...item, group: `${group}-overflow` })));
            }
        } else {
            mainData.push(...madaniSurahs.slice(0, maxSurahsPerRow));
            overflowData.push(...madaniSurahs.slice(maxSurahsPerRow).map(item => ({ ...item, group: `${group}-overflow` })));
            overflowData.push(...makkiSurahs.map(item => ({ ...item, group: `${group}-overflow` })));
        }
    });

    const mainDf = mainData;
    const overflowDf = overflowData;

    function calculatePositions(groupDf) {
        const uniqueGroups = [...new Set(groupDf.map(item => item.group))];
        uniqueGroups.forEach(group => {
            const groupData = groupDf.filter(item => item.group === group);
            const madaniSurahs = groupData.filter(item => item.makki_madani === 'Madani');
            const makkiSurahs = groupData.filter(item => item.makki_madani === 'Makki');

            const madaniCount = madaniSurahs.length;
            const makkiCount = makkiSurahs.length;

            const madaniStart = maxSurahsPerRow + 1 - madaniCount + 1;

            makkiSurahs.forEach((item, i) => item.position = i + 1);
            madaniSurahs.forEach((item, i) => item.position = madaniStart + i);
        });
    }

    calculatePositions(mainDf);
    calculatePositions(overflowDf);

    const groupsMain = [...new Set(mainDf.map(item => item.group))];
    const groupMappingMain = {};
    groupsMain.forEach((group, i) => groupMappingMain[group] = i + 1);
    mainDf.forEach(item => item.group = groupMappingMain[item.group]);

    const groupsOverflow = [...new Set(overflowDf.map(item => item.group))];
    const groupMappingOverflow = {};
    groupsOverflow.forEach((group, i) => groupMappingOverflow[group] = i + 1);
    overflowDf.forEach(item => item.group = groupMappingOverflow[item.group]);

    overflowDf.forEach((item, i) => item.position = (i % 17) + 1);
    overflowDf.forEach((item, i) => item.group = Math.floor(i / 17) + 1);

    const sourceMain = new Bokeh.ColumnDataSource({ data: mainDf });
    const sourceOverflow = new Bokeh.ColumnDataSource({ data: overflowDf });

    const pMain = new Bokeh.Plotting.figure({
        x_range: [0, 19],
        y_range: [Math.max(...mainDf.map(item => item.group)) + 1, 0],
        width: 900,
        height: 500,
        title: "Quran Surah Periodic Table",
        tools: "hover,reset,pan,wheel_zoom",
    });

    pMain.rect({
        x: { field: "position" },
        y: { field: "group" },
        width: 0.9,
        height: 0.9,
        source: sourceMain,
        fill_color: { field: "colors" },
        line_color: "black",
    });

    pMain.text({
        x: { field: "position" },
        y: { field: "group" },
        text: { field: "order" },
        source: sourceMain,
        text_align: "center",
        text_baseline: "middle",
        text_font_size: "12pt",
        y_offset: -16,
    });

    pMain.text({
        x: { field: "position" },
        y: { field: "group" },
        text: { field: "Symbol" },
        source: sourceMain,
        text_align: "center",
        text_baseline: "middle",
        text_font_size: "14pt",
        y_offset: 12,
    });

    pMain.xgrid.visible = false;
    pMain.ygrid.visible = false;
    pMain.xaxis.visible = false;
    pMain.yaxis.visible = false;

    const romanNumerals = ["I", "II", "III", "IV", "V", "VI", "VII"];
    groupsMain.forEach((groupNum, i) => {
        pMain.text({
            x: 0,
            y: groupNum,
            text: [romanNumerals[i]],
            text_align: "right",
            text_baseline: "middle",
            text_font_size: "14pt",
            x_offset: 0,
        });
    });

    const pOverflow = new Bokeh.Plotting.figure({
        x_range: [0, 18],
        y_range: [Math.max(...overflowDf.map(item => item.group)) + 1, 0],
        width: 900,
        height: 200,
        title: "Group VII (rest)",
        tools: "hover,reset,pan,wheel_zoom",
    });

    pOverflow.title.align = "center";

    pOverflow.rect({
        x: { field: "position" },
        y: { field: "group" },
        width: 0.9,
        height: 0.9,
        source: sourceOverflow,
        fill_color: { field: "colors" },
        line_color: "black",
    });

    pOverflow.text({
        x: { field: "position" },
        y: { field: "group" },
        text: { field: "order" },
        source: sourceOverflow,
        text_align: "center",
        text_baseline: "middle",
        text_font_size: "12pt",
        y_offset: -16,
    });

    pOverflow.text({
        x: { field: "position" },
        y: { field: "group" },
        text: { field: "Symbol" },
        source: sourceOverflow,
        text_align: "center",
        text_baseline: "middle",
        text_font_size: "14pt",
        y_offset: 12,
    });

    pOverflow.xgrid.visible = false;
    pOverflow.ygrid.visible = false;
    pOverflow.xaxis.visible = false;
    pOverflow.yaxis.visible = false;

    const hover = new Bokeh.Models.HoverTool({
        tooltips: [
            ["Name", "@name"],
            ["Ayat Count", "@ayat_count"],
            ["Makki/Madani", "@makki_madani"],
            ["Group", "@group"],
            ["Order", "@order"],
        ],
    });

    pMain.add_tools(hover);
    pOverflow.add_tools(hover);

    const grid = new Bokeh.Layouts.gridplot({ children: [[pMain], [pOverflow]] });

    Bokeh.embed.embedItem(grid, "plot");
})();