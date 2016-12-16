package com.sec.kanga.builder;

import backtype.storm.StormSubmitter;
import java.util.HashMap;
import backtype.storm.Config;
import backtype.storm.topology.TopologyBuilder;
import net.minidev.json.*;

import com.sec.kanga.common.*;
import com.sec.kanga.common.utils.KangaFactory;

/**
 * Created by amit1.nagar on 3/30/2016.
 */
public class SampleKangaTopology {

    public static void main(String[] args) throws Exception {

        String TOPOLOGY_NAME = "KangaTopology";
        TopologyBuilder topologyBuilder = new TopologyBuilder();
        HashMap paramMap = new HashMap();

        paramMap = new HashMap();
        paramMap.put("file_path", "/mnt/share/emp2.txt");
        paramMap.put("sleeping_time", "10");
        paramMap.put("output_name", "person");
        KangaSpout spout_flowchart_passthrough_from_file_174 = KangaFactory.getSpout("com.sec.kanga.spout.FileReaderSpout", paramMap);
        topologyBuilder.setSpout("flowchart_passthrough_from_file_174", spout_flowchart_passthrough_from_file_174, 1);

        paramMap = new HashMap();
        paramMap.put("condition", "person.salary>1000");
        paramMap.put("output_name", "output");
        KangaBolt bolt_flowchart_where_clause_30 = KangaFactory.getBolt("com.sec.kanga.bolt.filter.WhereClauseBolt", paramMap);
        topologyBuilder.setBolt("flowchart_where_clause_30", bolt_flowchart_where_clause_30, 1).shuffleGrouping("flowchart_passthrough_from_file_174");

        paramMap = new HashMap();
        paramMap.put("output_file_path", "/mnt/share/test_out.txt");
        paramMap.put("output_name", "out");
        KangaBolt bolt_flowchart_save_to_file_151 = KangaFactory.getBolt("com.sec.kanga.bolt.sink.SaveToFile", paramMap);
        topologyBuilder.setBolt("flowchart_save_to_file_151", bolt_flowchart_save_to_file_151, 1).shuffleGrouping("flowchart_where_clause_30");




        Config conf = new Config();
        conf.registerSerialization(JSONArray.class);
        conf.setDebug(false);
        conf.setNumWorkers(1);
//        conf.put(KangaLogger.KLOGGER_LEVEL, KangaLogger.Level.TRACE.severity());

        System.out.println("About to submit topology : " + TOPOLOGY_NAME);
        StormSubmitter.submitTopology(TOPOLOGY_NAME, conf, topologyBuilder.createTopology());
    }
}
