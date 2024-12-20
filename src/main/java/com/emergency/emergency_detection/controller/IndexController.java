package com.emergency.emergency_detection.controller;

import java.util.List;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.ModelAndView;

import com.emergency.emergency_detection.client.api.FastApiClient;
import com.emergency.emergency_detection.client.dto.HospitalResponse;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Controller
@RequiredArgsConstructor
@Slf4j
public class IndexController {

    private final FastApiClient fastApiClient;

    @GetMapping("/")
    public String index() {
        return "index";
    }

    @GetMapping("/recommend_hospital")
    public ModelAndView recommend_hospital(@RequestParam("request") String request, @RequestParam("latitude") double latitude, @RequestParam("longitude") double longitude) {
        List<HospitalResponse> hospitalList = fastApiClient.getHospital(request, latitude, longitude);
        log.info("hospital: {}", hospitalList);

        ModelAndView mv = new ModelAndView();
        mv.setViewName("recommend_hospital");
        mv.addObject("hospitalList", hospitalList);

        return mv;
    }
}

