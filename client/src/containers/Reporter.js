import React, {useState, useEffect, useRef, useCallback, useMemo} from "react";
import { Document, Page, Text, View, StyleSheet } from '@react-pdf/renderer';

const Reporter = React.memo(({nodes, dark}) => {

    const [groups, setGroups] = useState(new Map());

    const reportBlocksRef = useRef(new Map());

    useEffect(() => {
        if (nodes) {
            let mapper = new Map();
            nodes.forEach(function (node) {
                if (mapper.has(node['moduleName'])) {
                    let lst = mapper.get(node['moduleName']);
                    lst.push(node);
                    mapper.set(node['moduleName'], lst);
                } else {
                    let lst = [node];
                    mapper.set(node['moduleName'], lst);
                }
            });
            setGroups(mapper);
        }
    }, [nodes]);

    const styles = StyleSheet.create({
        doc: {
            flexDirection: "column"
        },
        page: {
            fontFamily: 'Helvetica',
            fontSize: 11,
            padding: 20,
            flexGrow: 1,
            flexDirection: 'column'
        },
        section: {
            marginBottom: 10,
            flexGrow: 1,
            flexDirection: 'column'
        },
        sectionTitle: {
            fontSize: 14,
            fontWeight: 'bold',
            marginBottom: 5,
        },
        subsection: {
            marginLeft: 10,
            marginBottom: 5,
            flexDirection: 'column',
            flexGrow: 1,
        },
        subsectionTitle: {
            fontSize: 12,
            fontWeight: 'bold',
            marginBottom: 3,
        },
        subsectionDetails: {
            fontSize: 11,
            lineHeight: 1.2,
        },
    });

    const report = useMemo(() => {
        let refnew = [];
        for (let [key, value] of groups.entries()) {
            let groupnew = (
                <View style={styles.section}>
                    <Text style={styles.sectionTitle}>{key}</Text>
                    {value.map(node => {

                        const variablesString = (node['variables'] ? node['variables'].join(", ") : "");
                        const callingString = (node['calls'] ? node['calls'].join(", ") : "");

                        return (
                            <View style={styles.subsection}>
                                <Text style={styles.subsectionTitle}>{node['functionName']}</Text>
                                <Text style={styles.subsectionDetails}>
                                    { node['endpoint']? "The function is an API endpoint": "" }
                                    The function is vulnerable due to its use of the variables {variablesString}, as they
                                    propagate into its use of the function(s) {callingString}.
                                </Text>
                            </View>
                        )
                    }) }
                </View>
            );
            refnew.push(groupnew);
        }
        return refnew;
    }, [groups, reportBlocksRef.current]);

    return (
        <Document style={styles.doc}>
            <Page style={styles.page}>
                {report}
            </Page>
        </Document>
    );
});

export default Reporter;